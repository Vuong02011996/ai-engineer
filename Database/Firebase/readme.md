# Using FireStore
+ Login vào firebase
+ Tạo project -> Project setting chọn web app
+ Chọn Build -> Cloud FiresStore -> Tạo db -> chọn vùng -> F5.
+ Đã tạo xong firestore trên firebase có thể đọc ghi dữ liệu lên firestore.
## Cấu trúc firestore
+ Gồm một tập hợp rất nhiều collection như là các bảng trong SQL.
+ Mỗi collection có rất nhiều documents.
## Javascript
+ Trong project FE: tạo file mới tên firebase/config.js trong src
+ Copy config trên web bỏ vào file config, export object db(firestore)ra ngoài sử dụng.
+ Ghi : `db.collection('tên_collection').add({dữ liệu cần ghi vào})`
+ Sử dụng hook useFireStore để lắng nghe dữ liệu thay đổi trên firestores.
## Python
+ Go to the Firebase Console and create a new project, or select an existing one.
+ Click on the gear icon on the left panel to go to the project settings.
+ Click on the "`Service Accounts`" tab, and then click on the "Generate new private key" button.
+ Save the generated JSON file to a secure location on your computer. 
This file contains your service account credentials, which you'll need to authenticate your application to Firebase.
+ Install the Firebase Admin SDK for Python: `pip install firebase-admin`
+ Tạo file config 
+ Write data to Firestore using the `set()` or `update()` method of the `DocumentReference` object.

# Setup emulator to test
+ Emulator sử dụng project trên firebase thực nên trước khi sử dụng emulator cần tạo project và đưa data lên db thật test trc.
+ Cài commandline của firebase: `sudo npm install -g firebase-tools`
+ Login: firebase login
+ Tạo new Project trên firebase.com
+ Init: firebase init -> cấu hình 
+ firebase emulators:start
