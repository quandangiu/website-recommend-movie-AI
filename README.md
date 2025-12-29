# Website Recommend Movie AI

## Giới thiệu
Website Recommend Movie AI là một hệ thống gợi ý phim thông minh sử dụng các thuật toán Machine Learning và AI để đề xuất phim phù hợp với sở thích của người dùng. Dự án được xây dựng trên nền tảng Django Framework và tích hợp nhiều thuật toán recommender systems như:

- **Collaborative Filtering**: Gợi ý dựa trên hành vi của người dùng tương tự
- **Content-Based Filtering**: Gợi ý dựa trên nội dung và đặc điểm của phim
- **Matrix Factorization**: Sử dụng FunkSVD để phân tích ma trận ratings
- **Association Rules**: Tìm mối liên hệ giữa các bộ phim
- **Clustering**: Phân nhóm người dùng theo sở thích

## Tính năng chính
- 🎬 Gợi ý phim cá nhân hóa cho từng người dùng
- 🔍 Tìm kiếm và khám phá phim mới
- ⭐ Đánh giá và theo dõi phim yêu thích
- 📊 Phân tích hành vi người dùng
- 🤖 Nhiều thuật toán AI/ML để gợi ý chính xác

## Dataset
Dự án sử dụng dataset [MovieTweetings](https://github.com/sidooms/MovieTweetings) và lấy thông tin phim, poster từ [TheMovieDB.org](https://www.themoviedb.org).

## Yêu cầu hệ thống
- Python 3.7 trở lên
- pip (Python package manager)
- Git
- SQLite3 (mặc định) hoặc PostgreSQL (khuyến nghị)

## Hướng dẫn cài đặt

### Bước 1: Clone repository
```bash
git clone https://github.com/quandangiu/website-recommend-movie-AI.git
cd website-recommend-movie-AI
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

**Trên Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Trên Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình API Key từ TheMovieDB

#### 4.1. Đăng ký tài khoản TheMovieDB
1. Truy cập [https://www.themoviedb.org/signup](https://www.themoviedb.org/signup)
2. Điền thông tin đăng ký và xác thực email

#### 4.2. Lấy API Key
1. Đăng nhập vào tài khoản TheMovieDB
2. Vào **Settings** (Cài đặt) → Click vào avatar góc trên bên phải → chọn **Settings**
3. Chọn **API** ở menu bên trái
4. Click vào **Create** hoặc **Request an API Key**
5. Chọn **Developer**
6. Điền thông tin:
   - **Application Name**: Website Recommend Movie AI (hoặc tên tùy ý)
   - **Application URL**: http://localhost:8000 (hoặc URL của bạn)
   - **Application Summary**: Movie recommendation system using AI
7. Đồng ý với điều khoản và submit
8. Copy **API Key (v3 auth)** hoặc **API Read Access Token**

#### 4.3. Cấu hình API Key vào project
Tạo file `.prs` trong thư mục gốc của project và thêm nội dung:
```json
{"themoviedb_apikey": "API_KEY_CỦA_BẠN_Ở_ĐÂY"}
```

**Ví dụ:**
```json
{"themoviedb_apikey": "a1sjbwofbiwhgbowijbwhvkbweo"}
```

⚠️ **Lưu ý:** 
- File `.prs` đã được thêm vào `.gitignore` để bảo mật
- Không share API key của bạn công khai
- Thay thế `API_KEY_CỦA_BẠN_Ở_ĐÂY` bằng API key thực tế

### Bước 5: Thiết lập Database

#### 5.1. Sử dụng SQLite (Mặc định - Đơn giản)
Django đã được cấu hình sẵn để sử dụng SQLite3. Tạo database và migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5.2. Sử dụng PostgreSQL (Khuyến nghị cho production)

**Cài đặt PostgreSQL:**
1. Download từ [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Cài đặt và khởi động PostgreSQL
3. Tạo database mới (sử dụng pgAdmin hoặc command line):
```sql
CREATE DATABASE moviegeek;
```

**Cài đặt driver PostgreSQL:**
```bash
pip install psycopg2
```

**Cấu hình trong `prs_project/settings.py`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'moviegeek',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Sau đó chạy migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 6: Import dữ liệu phim và ratings

⏱️ **Lưu ý:** Quá trình này có thể mất từ 10-30 phút tùy vào tốc độ mạng và máy tính.

```bash
python populate_moviegeek.py
python populate_ratings.py
```

Script sẽ tự động:
- Download dataset MovieTweetings
- Import thông tin phim vào database
- Import ratings của người dùng
- Lấy thông tin chi tiết và poster từ TheMovieDB API

### Bước 7: Khởi chạy web server

**Chạy server development:**
```bash
python manage.py runserver 127.0.0.1:8000
```

Hoặc chạy trên port khác nếu 8000 đã bị sử dụng:
```bash
python manage.py runserver 127.0.0.1:8001
```

🌐 **Truy cập website tại:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Bước 8: Tạo tài khoản admin (Optional)
Để truy cập Django Admin Panel:
```bash
python manage.py createsuperuser
```
Nhập username, email và password theo yêu cầu.

Truy cập admin tại: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Cách sử dụng

### 1. Khám phá phim
- Truy cập trang chủ để xem danh sách phim phổ biến
- Sử dụng thanh tìm kiếm để tìm phim theo tên
- Click vào poster phim để xem chi tiết

### 2. Đánh giá phim
- Vào trang chi tiết phim
- Chọn số sao để đánh giá (1-5 sao)
- Hệ thống sẽ ghi nhận và cập nhật gợi ý

### 3. Nhận gợi ý phim
- Sau khi đánh giá một số phim, hệ thống sẽ học sở thích của bạn
- Vào mục "Recommendations" để xem phim được gợi ý
- Phim được gợi ý dựa trên:
  - Các phim bạn đã đánh giá cao
  - Người dùng có sở thích tương tự
  - Nội dung và thể loại phim

### 4. Xem phân tích (Analytics)
Truy cập: [http://127.0.0.1:8000/analytics](http://127.0.0.1:8000/analytics)
- Xem biểu đồ độ tương đồng giữa các phim
- Phân tích nhóm người dùng (clustering)
- Xem topic modeling với LDA

## Training Models (Nâng cao)

Để cải thiện độ chính xác của gợi ý, chạy các thuật toán training:

### 1. Tính toán độ tương đồng giữa phim (Item Similarity)
```bash
python -m builder.item_similarity_calculator
```

### 2. Matrix Factorization (FunkSVD)
```bash
python -m builder.matrix_factorization_calculator
```

### 3. Association Rules
```bash
python -m builder.association_rules_calculator
```

### 4. User Clustering
```bash
python -m builder.user_cluster_calculator
```

### 5. Content-Based (LDA Model)
```bash
python -m builder.lda_model_calculator
```

### 6. Implicit Ratings
```bash
python -m builder.implicit_ratings_calculator
```

### 7. BPR (Bayesian Personalized Ranking)
```bash
python -m builder.bpr_calculator
```

## Tắt server và môi trường

**Dừng server:**
- Nhấn `Ctrl + C` trong terminal

**Thoát virtual environment:**
```bash
deactivate
```

## Troubleshooting

### Lỗi SSL Certificate (Mac OS)
Nếu gặp lỗi SSL khi chạy `populate_moviegeek.py`:
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Lỗi kết nối TheMovieDB API
- Kiểm tra API key trong file `.prs` có đúng không
- Kiểm tra kết nối internet
- API key có thể mất 10-15 phút để active sau khi tạo

### Database errors
- Xóa file `db.sqlite3` và chạy lại migrations
- Nếu dùng PostgreSQL, kiểm tra thông tin kết nối trong settings.py

## Công nghệ sử dụng

- **Backend**: Django 2.x, Python 3.x
- **Database**: SQLite3 / PostgreSQL
- **ML/AI Libraries**: 
  - scikit-learn (clustering, similarity)
  - NumPy, Pandas (data processing)
  - Gensim (LDA topic modeling)
  - implicit (BPR algorithm)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **API**: TheMovieDB API

## Tác giả & Đóng góp

Dự án được phát triển dựa trên framework của [Practical Recommender Systems](https://github.com/practical-recommender-systems/moviegeek)

Mọi đóng góp và cải thiện đều được chào đón. Hãy tạo Pull Request hoặc Issue nếu bạn có ý tưởng!

## License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

⭐ **Nếu thấy project hữu ích, đừng quên cho một star nhé!**
