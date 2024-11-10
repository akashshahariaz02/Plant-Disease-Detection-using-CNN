import os
import json
from PIL import Image

import numpy as np
import tensorflow as tf
import streamlit as st

# Define class names
CLASS_NAMES = ["অ্যাপল স্ক্যাব", "অ্যাপল ব্ল্যাক রট", "আপেল মরিচা", "আপেল সুস্থ", "ব্লুবেরি সুস্থ",
                "চেরি পাউডারি মিলডিউ", "চেরি সুস্থ",
                "ভুট্টা ধূসর পাতার দাগ",
                "ভুট্টার সাধারণ মরিচা", "ভুট্টার নর্দার্ন লিফ ব্লাইট", "ভুট্টা সুস্থ",
                "আঙ্গুর কালো পচা", "আঙ্গুর এসকা",
                "আঙ্গুর পাতার ব্লাইট", "আঙ্গুর সুস্থ",
                "কমলা হাংলংবিং(সাইট্রাস_সবুজ)",
                "পীচ ব্যাকটেরিয়াল স্পট", "পিচ সুস্থ", "পেপারবেল ব্যাকটেরিয়াল স্পট", "পিপারবেল সুস্থ",
                "আলু প্রারম্ভিক ব্লাইট", "আলু দেরী ব্লাইট", "আলু সুস্থ", "রাস্পবেরি সুস্থ",
                "সয়াবিন সুস্থ", "স্কোয়াশ পাউডারি মিলডিউ", "স্ট্রবেরি সুস্থ", "স্ট্রবেরি পাতা ঝলসানো",
                "টমেটো ব্যাকটেরিয়াল স্পট", "টমেটো আর্লি ব্লাইট", "টমেটো লেট ব্লাইট", "টমেটো লিফ মোল্ড",
                "টমেটো সেপ্টোরিয়া পাতার দাগ", "টমেটো স্পাইডার মাইটস",
                "টমেটো টার্গেট স্পট", "টমেটো ইয়েলো লিফ কার্ল ভাইরাস",
                "টমেটো মোজাইক ভাইরাস", "টমেটো সুস্থ"]

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{working_dir}/trained_model/plant_disease_prediction_model.h5"

# Load the pre-trained model
model = tf.keras.models.load_model(model_path)

# Loading the class indices
class_indices = json.load(open(f"{working_dir}/class_indices.json"))

# Function to Load and Preprocess the Image using Pillow
def load_and_preprocess_image(image_path, target_size=(224, 224)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.
    return img_array

# Function to Predict the Class of an Image
def predict_image_class(model, image_path, class_indices):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = CLASS_NAMES[predicted_class_index]
    return predicted_class_name

# Plant disease solutions
disease_solutions = {
    'অ্যাপল ব্ল্যাক রট': 'রাসায়নিক চিকিৎসা: অ্যাপল ব্ল্যাক রট নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল যেমন ক্রমিয়ান, ফেনভালেট, মালাথাইন, পাইপেরাফস, সাইপারমেথ্রিন ইত্যাদি ব্যবহার করা হতে পারে।',
    'অ্যাপল স্ক্যাব': 'রাসায়নিক চিকিৎসা: সানেচার ব্যবহার করে স্ক্যাবের বিস্তার ও বাহিত রোগাণুগুলি কমানো যেতে পারে। স্ক্যাবের প্রতিরোধ করার জন্য প্রোফিলাক্টিক রোগনিরাপত্তা চিকিৎসা অনুমোদিত হতে পারে।',
    'আপেল মরিচ রোগ': 'রাসায়নিক চিকিৎসা: আপেল মরিচ রোগ নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল ব্যবহার করা হতে পারে, যেমন ক্রমিয়ান, ফেনভালেট, মালাথাইন, পাইপেরাফস, সাইপারমেথ্রিন ইত্যাদি ব্যবহার করা হতে পারে।',
    'আপেল সুস্থ': 'সুস্থ',
    'ব্লুবেরি সুস্থ': 'সুস্থ',
    'চেরি পাউডারি মিলডিউ': 'রাসায়নিক চিকিৎসা: চেরি পাউডারি মিলডিউ নিয়ন্ত্রণের জন্য বিভিন্ন রাসায়নিক যেমন ক্রমিয়ান, ফেনভালেট, মানেব, পাইপেরাফস, সাইপারমেথ্রিন ইত্যাদি ব্যবহার করা হতে পারে।',
    'চেরি সুস্থ': 'সুস্থ',
    'ভুট্টা ধূসর পাতার দাগ': 'রাসায়নিক চিকিৎসা: ভুট্টা ধূসর পাতার দাগ নিয়ন্ত্রণের জন্য সাক্রিয় কেমিক্যাল ব্যবহার করা হতে পারে, যেমন ক্যাপটান, ম্যানকোজেব, বেঞ্জিমাইট, অক্সিক্লোরাইড, মানেব, পাইপেরাফস, ফুলাইয়াইট, স্পিনোসাড, ট্রায়াজোল, ইট্রাকোনাজোল, সাইপারমেথ্রিন, ইত্যাদি।',
    'ভুট্টার সাধারণ মরিচা': 'রাসায়নিক চিকিৎসা: ভুট্টার সাধারণ মরিচা নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল ব্যবহার করা হতে পারে, যেমন ক্রমিয়ান, ফেনভালেট, মালাথাইন, পাইপেরাফস, সাইপারমেথ্রিন ইত্যাদি।',
    'ভুট্টার নর্দার্ন লিফ ব্লাইট': 'রাসায়নিক চিকিৎসা: রোগ নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল ব্যবহার করা হতে পারে, যেমন সাইপারমেথ্রিন, ক্রমিয়ান, ফেনভালেট, মালাথাইন, পাইপেরাফস ইত্যাদি।',
    'ভুট্টা সুস্থ': 'সুস্থ',
    'আঙ্গুর কালো পচা': 'রাসায়নিক চিকিৎসা: আঙ্গুর কালো পচা রোগের নির্ভরশীল রোগনিরাপত্তা চিকিৎসার জন্য সক্রিয় রাসায়নিক যেমন কাপটান, ম্যানকোজেব, সুলফার ইত্যাদি ব্যবহার করা হতে পারে।',
    'আঙ্গুর এসকা': 'রাসায়নিক চিকিৎসা: রোগ নিয়ন্ত্রণে ক্যাপটান, ম্যানকোজেব, থায়ামেথক্সাম, সুলফার এবং ক্যালসিয়াম কার্বাইড সহ কিছু কেমিক্যাল ব্যবহার করা যেতে পারে।',
    'আঙ্গুর পাতার ব্লাইট': 'রাসায়নিক চিকিৎসা: আঙ্গুর পাতার ব্লাইট নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল ব্যবহার করা হতে পারে, যেমন কোপার অক্সিক্লোরাইড, ম্যানকেব, টেট্রাকনাজোল, টেবুকোনাজোল, প্রোপিকোনাজোল, সাইপারমেথ্রিন ইত্যাদি।',
    'আঙ্গুর সুস্থ': 'সুস্থ',
    'কমলা হাংলংবিং(সাইট্রাস_সবুজ)': 'রাসায়নিক চিকিৎসা: কমলা হাংলংবিং(সাইট্রাস_সবুজ) নিয়ন্ত্রণের জন্য সক্রিয় কেমিক্যাল যেমন থিওফানেট-মেথাইল, অক্সিক্লোরাইডিন, মানেব, সিপারমিথিন ইত্যাদি ব্যবহার করা হতে পারে।',
    'পীচ ব্যাকটেরিয়াল স্পট': 'রাসায়নিক চিকিৎসা: পীচ ব্যাকটেরিয়াল স্পট নিয়ন্ত্রণের জন্য ক্রমিয়ান, ফেনভালেট, মালাথাইন, পাইপেরাফস, সাইপারমেথ্রিন ইত্যাদি সক্রিয় রাসায়নিক যন্ত্রপাতি ব্যবহার করা হতে পারে।',
    'পীচ সুস্থ': 'সুস্থ',
    'পেপারবেল ব্যাকটেরিয়াল স্পট': 'রাসায়নিক চিকিৎসা: ব্লাইটের নিয়ন্ত্রণে এবং ব্যাকটেরিয়াল স্পটের জন্য সানেচার এবং ব্যবহার করা যেতে পারে, এছাড়াও কয়েকটি প্রক্রিয়ার জন্য সক্রিয় রাসায়নিক যেমন কপার হাইড্রক্সাইড, ম্যানকেব, কপার অক্সিক্লোরাইড, বর্তমান ব্লাইট নিয়ন্ত্রণে ব্যবহৃত হয়েছে, এটি অক্সিক্লোরাইড, ম্যানকেব, ক্যাপটান এবং সাফলফারের মধ্যে প্রযোজ্য হতে পারে।',
    'পিপারবেল সুস্': 'সুস্থ',
    'আলু আর্লি ব্লাইট ': 'রাসায়নিক চিকিৎসা: আলু আর্লি ব্লাইট নিয়ন্ত্রণের জন্য ফসলের সানেচার এবং প্রতিরোধ করার জন্য ফসল প্রোফিলাক্টিক চিকিৎসা প্রযোজ্য হতে পারে।',
    'আলু লেট ব্লাইট ': 'রাসায়নিক চিকিৎসা: আলু লেট ব্লাইট নির্গত করার জন্য সক্রিয় কেমিক্যাল পদক্ষেপ অনুমোদিত হতে পারে, যেমন কোপার সালফেট, ক্রমিয়ান, মালাথাইন, ফেনভালেট, মানকোজেব ইত্যাদি।',
    'আলু সুস্থ': 'সুস্থ',
    'রাস্পবেরি সুস্থ': 'সুস্থ',
    'সয়াবিন সুস্থ': 'সুস্থ',
    'স্কোয়াশ পাউডারি মিলডিউ':'রাসায়নিক চিকিৎসা: পাউডারি মিলডিউ প্রতিরোধের জন্য সালফার বা ক্যালসিয়াম কার্বোনেট প্রয়োগ করা যেতে পারে। আরও উন্নত চিকিৎসার জন্য বায়োকন্ট্রোল এজেন্ট যেমন ট্রাইকোডার্মা ব্যবহার করা যেতে পারে।',
    'স্ট্রবেরি সুস্থ': 'সুস্থ',
    'স্ট্রবেরি পাতা ঝলসানো': 'রাসায়নিক চিকিৎসা: পাতা ঝলসানো প্রতিরোধের জন্য কপার ভিত্তিক ফাঙ্গিসাইড ব্যবহার করা যেতে পারে। এছাড়া, খনিজ তেল ও জৈবিক ফাঙ্গিসাইড যেমন নিওনিওটিনোয়েড ব্যবহারের সুপারিশ করা হয়।',
    'টমেটো ব্যাকটেরিয়াল স্পট': 'রাসায়নিক চিকিৎসা: ব্যাকটেরিয়াল স্পট নিয়ন্ত্রণের জন্য কপার ভিত্তিক ব্যাকটেরিসাইড ব্যবহার করা যেতে পারে। এছাড়া, স্ট্রেপ্টোমাইসিন সালফেট ও অক্সিটেট্রাসাইক্লিন ব্যবহারের সুপারিশ করা হয়।',
    'টমেটো আর্লি ব্লাইট': 'রাসায়নিক চিকিৎসা: আর্লি ব্লাইট প্রতিরোধের জন্য ক্লোরোথালোনিল বা মানকোজেব ফাঙ্গিসাইড ব্যবহার করা যেতে পারে।',
    'টমেটো লেট ব্লাইট': 'রাসায়নিক চিকিৎসা: লেট ব্লাইট প্রতিরোধের জন্য মেটালাক্সিল এবং মানকোজেব ফাঙ্গিসাইড ব্যবহার করা যেতে পারে।',
    'টমেটো লিফ মোল্ড': 'রাসায়নিক চিকিৎসা: লিফ মোল্ড নিয়ন্ত্রণের জন্য কপার অক্সিক্লোরাইড বা চিটোসান ভিত্তিক ফাঙ্গিসাইড ব্যবহার করা যেতে পারে।',
    'টমেটো সেপ্টোরিয়া পাতার দাগ': 'রাসায়নিক চিকিৎসা: সেপ্টোরিয়া পাতার দাগ প্রতিরোধের জন্য ক্লোরোথালোনিল বা ডাইক্যাপ্টেন ব্যবহারের সুপারিশ করা হয়।',
    'টমেটো স্পাইডার মাইটস': 'রাসায়নিক চিকিৎসা: স্পাইডার মাইটস নিয়ন্ত্রণের জন্য অ্যাবামেকটিন বা সপ ব্যবহারের সুপারিশ করা হয়।',
    'টমেটো টার্গেট স্পট': 'রাসায়নিক চিকিৎসা: টার্গেট স্পট নিয়ন্ত্রণের জন্য ম্যানকোজেব এবং ক্লোরোথালোনিল ফাঙ্গিসাইড ব্যবহার করা যেতে পারে।',
    'টমেটো ইয়েলো লিফ কার্ল ভাইরাস': 'রাসায়নিক চিকিৎসা: ইয়েলো লিফ কার্ল ভাইরাস প্রতিরোধের জন্য রেসিস্ট্যান্ট জাত ব্যবহারের পাশাপাশি থায়ামেথক্সাম ভিত্তিক ইনসেক্টিসাইড ব্যবহারের সুপারিশ করা হয়।',
    'টমেটো মোজাইক ভাইরাস': 'রাসায়নিক চিকিৎসা: মোজাইক ভাইরাস প্রতিরোধের জন্য রোগমুক্ত বীজ ব্যবহার এবং এফিড প্রতিরোধে ইমিডাক্লোপ্রিড ব্যবহার করা যেতে পারে।',
    'টমেটো সুস্থ': 'সুস্থ'
}

# Streamlit App
st.title('🌿উদ্ভিদ রোগ শনাক্তকারী')
uploaded_image = st.file_uploader("একটি ছবি আপলোড করুন...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    col1, col2 = st.columns(2)

    with col1:
        resized_img = image.resize((150, 150))
        st.image(resized_img)

    with col2:
        if st.button('শনাক্ত করুন'):
            # Preprocess the uploaded image and predict the class
            prediction = predict_image_class(model, uploaded_image, class_indices)
            st.success(f'ফলাফল: {prediction}')

            # Display solution for the predicted class if available
            if prediction in disease_solutions:
                solution = disease_solutions[prediction]
                if isinstance(solution, dict):
                    option = st.radio("সমাধান নির্বাচন করুন:", list(solution.keys()))
                    st.write("সমাধান:", solution[option])
                else:
                    st.write("সমাধান:", solution)
            else:
                st.write("এই শ্রেণীর জন্য কোন সমাধান পাওয়া যায় নি।")

