# HƯỚNG DẪN CHẠY ITEM SIMILARITY CALCULATOR

## Mục đích
File `item_similarity_calculator.py` dùng để tính toán độ tương đồng giữa các bộ phim dựa trên đánh giá của người dùng. Kết quả được lưu vào database để phục vụ cho hệ thống gợi ý phim.

## Yêu cầu trước khi chạy

### 1. Cài đặt môi trường Python
Đảm bảo đã cài đặt Python và các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình Database
- Database phải được thiết lập đúng trong `prs_project/settings.py`
- Hỗ trợ 2 loại database:
  - PostgreSQL (khuyên dùng cho production)
  - SQLite3 (dùng cho development)

### 3. Có dữ liệu đánh giá
Phải có dữ liệu trong bảng `Rating` (analytics_rating). Nếu chưa có, chạy:
```bash
python populate_ratings.py
```

## Các cách chạy

### Cách 1: Chạy trực tiếp từ command line
```bash
python -m builder.item_similarity_calculator
```

### Cách 2: Chạy từ thư mục builder
```bash
cd builder
python item_similarity_calculator.py
```

### Cách 3: Chạy với Docker
Nếu bạn đang sử dụng Docker:

#### 3.1. Kiểm tra container đang chạy
```bash
docker ps
```

#### 3.2. Chạy lệnh trong Docker container
```bash
# Thay <container_name> bằng tên container của bạn
docker exec -it <container_name> python -m builder.item_similarity_calculator
```

#### 3.3. Hoặc vào shell của container
```bash
docker exec -it <container_name> bash
python -m builder.item_similarity_calculator
```

#### 3.4. Nếu sử dụng docker-compose
```bash
docker-compose exec web python -m builder.item_similarity_calculator
```

### Cách 4: Import và chạy từ Python shell
```python
from builder.item_similarity_calculator import ItemSimilarityMatrixBuilder, load_all_ratings

# Tải dữ liệu đánh giá
ratings = load_all_ratings()

# Tạo builder với các tham số tùy chỉnh
builder = ItemSimilarityMatrixBuilder(min_overlap=5, min_sim=0.1)

# Chạy tính toán và lưu vào database
builder.build(ratings, save=True)
```

## Các tham số có thể điều chỉnh

### min_overlap (mặc định = 5)
- Số lượng user tối thiểu phải đánh giá cả 2 phim
- **Càng cao**: Chất lượng càng tốt nhưng ít kết quả hơn
- **Càng thấp**: Nhiều kết quả hơn nhưng kém tin cậy
- **Khuyến nghị**: 5-10

### min_sim (mặc định = 0.1)
- Ngưỡng độ tương đồng tối thiểu (từ 0 đến 1)
- **Càng cao**: Chỉ lưu các phim rất giống nhau
- **Càng thấp**: Lưu nhiều kết quả hơn
- **Khuyến nghị**: 0.1-0.3

## Ví dụ chạy với các tham số khác

### Chất lượng cao (ít kết quả, độ tin cậy cao)
```python
from builder.item_similarity_calculator import ItemSimilarityMatrixBuilder, load_all_ratings

ratings = load_all_ratings()
builder = ItemSimilarityMatrixBuilder(min_overlap=10, min_sim=0.3)
builder.build(ratings, save=True)
```

### Nhiều kết quả (chất lượng trung bình)
```python
from builder.item_similarity_calculator import ItemSimilarityMatrixBuilder, load_all_ratings

ratings = load_all_ratings()
builder = ItemSimilarityMatrixBuilder(min_overlap=2, min_sim=0.05)
builder.build(ratings, save=True)
```

## Quá trình xử lý

Khi chạy, chương trình sẽ thực hiện các bước sau:

1. **Load dữ liệu**: Tải tất cả đánh giá từ database
2. **Chuẩn hóa**: Chuẩn hóa điểm đánh giá của mỗi user
3. **Tạo ma trận**: Tạo ma trận sparse (thưa) để tiết kiệm bộ nhớ
4. **Tính overlap**: Xác định số user đánh giá chung giữa các cặp phim
5. **Tính similarity**: Tính độ tương đồng cosine giữa các phim
6. **Lọc kết quả**: Chỉ giữ các cặp phim thỏa mãn min_overlap và min_sim
7. **Lưu database**: Lưu kết quả vào bảng `Similarity` (recommender_similarity)

## Output / Kết quả

### Log trong quá trình chạy
```
Calculating similarities ... using 100000 ratings
Creating ratings matrix
Calculating overlaps between the items
Overlap matrix leaves 3000000 out of 40000000 with 5
Rating matrix (size 1000x10000) finished, in 10 seconds
Sparsity level is 0.99
Correlation is finished, done in 30 seconds
3000000 similarities to save
Similarity items saved, done in 120 seconds
```

### Dữ liệu trong database
Bảng `similarity` sẽ chứa:
- `source`: ID phim nguồn
- `target`: ID phim đích
- `similarity`: Độ tương đồng (0-1)
- `created`: Thời gian tạo

Ví dụ:
```
source  | target | similarity | created
--------|--------|------------|-------------------
1       | 50     | 0.8        | 2025-10-21 10:00:00
1       | 150    | 0.75       | 2025-10-21 10:00:00
2       | 100    | 0.6        | 2025-10-21 10:00:00
```

## Thời gian chạy

Thời gian phụ thuộc vào:
- Số lượng đánh giá
- Số lượng phim
- Số lượng user
- Cấu hình máy

**Ước tính**:
- 10,000 ratings: ~30 giây
- 100,000 ratings: ~5 phút
- 1,000,000 ratings: ~30 phút
- 10,000,000 ratings: ~4 giờ

## Xử lý lỗi thường gặp

### Lỗi: No module named 'django'
```bash
pip install django
```

### Lỗi: No module named 'sklearn'
```bash
pip install scikit-learn
```

### Lỗi khi dùng Docker

#### Container không chạy
```bash
# Kiểm tra container
docker ps -a

# Start container nếu đang dừng
docker start <container_name>

# Hoặc restart
docker restart <container_name>
```

#### Lỗi: Database connection refused trong Docker
```bash
# Kiểm tra database container có chạy không
docker ps | grep postgres

# Kiểm tra network
docker network ls
docker network inspect <network_name>

# Restart cả database và web container
docker-compose restart
```

#### Lỗi: Permission denied trong Docker
```bash
# Chạy với quyền root
docker exec -u root -it <container_name> python -m builder.item_similarity_calculator

# Hoặc sửa quyền file
docker exec -it <container_name> chmod -R 755 /app
```

#### Lỗi: Out of memory trong Docker
```bash
# Tăng memory limit cho container trong docker-compose.yml
# Thêm vào service:
#   mem_limit: 4g
#   memswap_limit: 4g

# Hoặc khi chạy docker run
docker run -m 4g --memory-swap 4g ...
```

### Lỗi: Out of memory
Giảm số lượng dữ liệu hoặc tăng min_overlap:
```python
ratings = load_all_ratings(min_ratings=5)  # Chỉ lấy user có ít nhất 5 ratings
builder = ItemSimilarityMatrixBuilder(min_overlap=10, min_sim=0.2)
```

## Kiểm tra kết quả
# Có thể vào bảng "similarity" xem nó đã có dữ liệu chưa. 

### Từ Python shell
```python
from recommender.models import Similarity

# Đếm số lượng similarities
count = Similarity.objects.count()
print(f"Tổng số similarities: {count}")

# Xem top 10 cặp phim tương đồng nhất
top_sims = Similarity.objects.order_by('-similarity')[:10]
for sim in top_sims:
    print(f"Phim {sim.source} ↔ Phim {sim.target}: {sim.similarity}")

# Tìm các phim tương tự với phim ID = 1
similar_movies = Similarity.objects.filter(source=1).order_by('-similarity')[:5]
for sim in similar_movies:
    print(f"Phim {sim.target}: {sim.similarity}")
```

### Từ Django shell
```bash
python manage.py shell
```
```python
from recommender.models import Similarity
print(Similarity.objects.count())
```

### Kiểm tra trong Docker

#### Vào Django shell trong container
```bash
docker exec -it <container_name> python manage.py shell
```
```python
from recommender.models import Similarity
print(f"Tổng số similarities: {Similarity.objects.count()}")
```

#### Kiểm tra database trực tiếp (PostgreSQL)
```bash
# Vào PostgreSQL container
docker exec -it <postgres_container_name> psql -U <username> -d <database_name>

# Chạy query
SELECT COUNT(*) FROM recommender_similarity;
SELECT * FROM recommender_similarity ORDER BY similarity DESC LIMIT 10;
```

#### Kiểm tra database trực tiếp (SQLite)
```bash
# Vào container
docker exec -it <container_name> bash

# Mở SQLite
sqlite3 db.sqlite3

# Chạy query
SELECT COUNT(*) FROM recommender_similarity;
SELECT * FROM recommender_similarity ORDER BY similarity DESC LIMIT 10;
```

#### Xem logs của container
```bash
# Xem logs real-time
docker logs -f <container_name>

# Xem 100 dòng logs cuối
docker logs --tail 100 <container_name>
```

## Chạy lại / Cập nhật

Khi có dữ liệu đánh giá mới:
1. Chạy lại script để cập nhật similarities
2. Dữ liệu cũ sẽ tự động bị xóa (truncate)
3. Dữ liệu mới được tính toán và lưu vào

### Chạy thông thường
```bash
python -m builder.item_similarity_calculator
```

### Chạy trong Docker
```bash
# Với docker exec
docker exec -it <container_name> python -m builder.item_similarity_calculator

# Với docker-compose
docker-compose exec web python -m builder.item_similarity_calculator

# Chạy background (không block terminal)
docker exec -d <container_name> python -m builder.item_similarity_calculator
```

### Thiết lập chạy định kỳ trong Docker

#### Sử dụng cron trong container
```bash
# Vào container
docker exec -it <container_name> bash

# Cài cron (nếu chưa có)
apt-get update && apt-get install -y cron

# Tạo cron job
crontab -e

# Thêm dòng này để chạy mỗi tuần (Chủ nhật 2 AM)
0 2 * * 0 cd /app && python -m builder.item_similarity_calculator >> /var/log/similarity.log 2>&1
```

#### Sử dụng host cron (khuyến nghị)
Trên máy host (Windows/Linux/Mac), tạo script:

**Linux/Mac:**
```bash
# Tạo file run_similarity.sh
#!/bin/bash
docker exec <container_name> python -m builder.item_similarity_calculator

# Chmod
chmod +x run_similarity.sh

# Thêm vào crontab
crontab -e
0 2 * * 0 /path/to/run_similarity.sh >> /var/log/similarity.log 2>&1
```

**Windows (Task Scheduler):**
```powershell
# Tạo file run_similarity.bat
docker exec <container_name> python -m builder.item_similarity_calculator

# Sau đó tạo Scheduled Task trong Windows Task Scheduler
```

## Best Practices (Khuyến nghị)

1. **Chạy định kỳ**: Nên chạy lại mỗi tuần hoặc khi có nhiều đánh giá mới
2. **Backup trước**: Backup database trước khi chạy
3. **Chạy off-peak**: Chạy vào lúc ít người dùng để tránh ảnh hưởng hiệu suất
4. **Monitor logs**: Theo dõi logs để phát hiện lỗi sớm
5. **Test parameters**: Thử nghiệm với tham số khác nhau để tìm ra cấu hình tối ưu

## Tích hợp với hệ thống gợi ý

Sau khi chạy xong, dữ liệu similarities sẽ được sử dụng bởi:
- `neighborhood_based_recommender.py`: Đề xuất phim dựa trên độ tương đồng
- `content_based_recommender.py`: Gợi ý phim tương tự

Ví dụ sử dụng trong recommender:
```python
from recs.neighborhood_based_recommender import NeighborhoodBasedRecs

recommender = NeighborhoodBasedRecs(neighborhood_size=20, min_sim=0.1)
recommendations = recommender.recommend_items(user_id=1, num=10)
print(recommendations)
```

## Liên hệ / Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Log output để xem lỗi chi tiết
2. Database có đủ dữ liệu không
3. Tham số có phù hợp với dataset không
4. Cấu hình Django settings có đúng không
