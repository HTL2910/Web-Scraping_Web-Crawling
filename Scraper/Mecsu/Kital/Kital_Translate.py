import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import time

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. Đọc dữ liệu từ Excel
def load_data_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    print(f"Loaded {len(df)} records from Excel file")
    return df

# 2. Tải và lưu hình ảnh
def download_images(df, image_dir="product_images"):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    image_paths = []
    
    for idx, row in df.iterrows():
        product_name = row['Name']
        image_url = row['Image Link']
        
        # Tạo tên file an toàn từ tên sản phẩm
        safe_name = "".join([c if c.isalnum() else "_" for c in product_name])
        image_path = os.path.join(image_dir, f"{idx}_{safe_name}.jpg")
        
        # Kiểm tra nếu ảnh đã tồn tại
        if os.path.exists(image_path):
            image_paths.append(image_path)
            continue
            
        try:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.save(image_path)
            image_paths.append(image_path)
            print(f"Downloaded {idx+1}/{len(df)}: {product_name}")
            time.sleep(0.1)  # Tránh request quá nhanh
        except Exception as e:
            print(f"Error downloading {product_name}: {e}")
            image_paths.append(None)
    
    # Thêm đường dẫn hình ảnh vào DataFrame
    df['Image Path'] = image_paths
    df = df.dropna(subset=['Image Path'])  # Loại bỏ các hàng không có hình ảnh
    
    return df

# 3. Tiền xử lý hình ảnh và chuẩn bị dữ liệu cho mô hình
def prepare_data(df, img_size=(224, 224)):
    # Mã hóa nhãn (tên sản phẩm)
    label_encoder = LabelEncoder()
    df['Label'] = label_encoder.fit_transform(df['Name'])
    
    # Lưu lại ánh xạ từ số -> tên sản phẩm để dùng khi dự đoán
    label_mapping = dict(zip(df['Label'], df['Name']))
    
    # Chia dữ liệu thành train, validation và test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        df['Image Path'], df['Label'], test_size=0.15, random_state=42, stratify=df['Label'] if len(df) > len(set(df['Label'])) * 2 else None
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.15, random_state=42, stratify=y_train_val if len(y_train_val) > len(set(y_train_val)) * 2 else None
    )
    
    # Tạo các DataFrame cho từng tập dữ liệu
    train_df = pd.DataFrame({'Image Path': X_train, 'Label': y_train})
    val_df = pd.DataFrame({'Image Path': X_val, 'Label': y_val})
    test_df = pd.DataFrame({'Image Path': X_test, 'Label': y_test})
    
    # Tạo data generator với augmentation cho tập train
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Data generator cho validation và test (chỉ rescale)
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Chuẩn bị các generator
    batch_size = 32
    
    def load_image(img_path):
        img = Image.open(img_path).convert('RGB')
        img = img.resize(img_size)
        return np.array(img)
    
    train_generator = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        x_col='Image Path',
        y_col='Label',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='sparse',
        shuffle=True
    )
    
    validation_generator = val_test_datagen.flow_from_dataframe(
        dataframe=val_df,
        x_col='Image Path',
        y_col='Label',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='sparse',
        shuffle=False
    )
    
    test_generator = val_test_datagen.flow_from_dataframe(
        dataframe=test_df,
        x_col='Image Path',
        y_col='Label',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='sparse',
        shuffle=False
    )
    
    return train_generator, validation_generator, test_generator, label_encoder, label_mapping

# 4. Xây dựng và huấn luyện mô hình
def create_model(num_classes):
    # Sử dụng EfficientNetB0 làm backbone, có thể thay bằng ResNet50, MobileNet, v.v.
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Đóng băng các lớp của model pre-trained
    for layer in base_model.layers:
        layer.trainable = False
    
    # Thêm các lớp mới
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Biên dịch mô hình
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model(model, train_generator, validation_generator, epochs=10):
    # Thiết lập callbacks
    checkpoint = ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        mode='max',
        verbose=1
    )
    
    # Huấn luyện mô hình
    history = model.fit(
        train_generator,
        steps_per_epoch=len(train_generator),
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=len(validation_generator),
        callbacks=[checkpoint, early_stopping]
    )
    
    return model, history

# 5. Đánh giá mô hình
def evaluate_model(model, test_generator, label_mapping):
    # Đánh giá mô hình trên tập test
    test_loss, test_accuracy = model.evaluate(test_generator)
    print(f"Test accuracy: {test_accuracy:.4f}")
    
    # Dự đoán trên tập test
    predictions = model.predict(test_generator)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Lấy ground truth
    true_classes = test_generator.classes
    
    # Hiển thị một số dự đoán
    for i in range(min(10, len(predicted_classes))):
        true_label = label_mapping[true_classes[i]]
        predicted_label = label_mapping[predicted_classes[i]]
        print(f"True: {true_label} | Predicted: {predicted_label}")
    
    return test_accuracy

# 6. Hàm dự đoán tên sản phẩm từ đường dẫn hình ảnh
def predict_product_name(model, image_url, label_mapping, img_size=(224, 224)):
    try:
        # Tải hình ảnh từ URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        
        # Tiền xử lý
        img = img.resize(img_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Dự đoán
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        
        # Lấy tên sản phẩm
        product_name = label_mapping[predicted_class]
        confidence = prediction[0][predicted_class]
        
        return product_name, confidence
    
    except Exception as e:
        print(f"Error predicting image: {e}")
        return None, 0

# 7. Chức năng cập nhật Excel với dự đoán
def update_excel_with_predictions(input_excel, output_excel, model, label_mapping):
    # Đọc file Excel
    df = pd.read_excel(input_excel)
    
    # Thêm cột dự đoán và độ tin cậy
    df['Predicted Name'] = None
    df['Confidence'] = None
    
    for idx, row in df.iterrows():
        image_url = row['Image Link']
        product_name, confidence = predict_product_name(model, image_url, label_mapping)
        
        df.at[idx, 'Predicted Name'] = product_name
        df.at[idx, 'Confidence'] = confidence
        
        if idx % 10 == 0:
            print(f"Processed {idx+1}/{len(df)} images")
    
    # Lưu kết quả
    df.to_excel(output_excel, index=False)
    print(f"Predictions saved to {output_excel}")

# Hàm chính để chạy toàn bộ quy trình
def main():
    # Đường dẫn file Excel
    excel_path = "your_product_data.xlsx"  # Thay đổi đường dẫn này
    
    # 1. Đọc dữ liệu
    df = load_data_from_excel(excel_path)
    
    # 2. Tải hình ảnh
    df = download_images(df)
    
    # 3. Chuẩn bị dữ liệu
    train_gen, val_gen, test_gen, label_encoder, label_mapping = prepare_data(df)
    
    # 4. Tạo và huấn luyện mô hình
    num_classes = len(label_mapping)
    model = create_model(num_classes)
    
    # Hiển thị tóm tắt mô hình
    model.summary()
    
    # 5. Huấn luyện mô hình
    model, history = train_model(model, train_gen, val_gen, epochs=20)
    
    # 6. Đánh giá mô hình
    evaluate_model(model, test_gen, label_mapping)
    
    # 7. Lưu mô hình và label_mapping để sử dụng sau này
    model.save('product_recognition_model.h5')
    
    # Lưu label_mapping
    with open('label_mapping.txt', 'w') as f:
        for label, name in label_mapping.items():
            f.write(f"{label},{name}\n")
    
    # 8. Cập nhật file Excel với dự đoán
    update_excel_with_predictions(excel_path, "predicted_products.xlsx", model, label_mapping)

# Chạy chương trình
if __name__ == "__main__":
    main()