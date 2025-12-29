import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prs_project.settings")
django.setup()

from recommender.models import MovieDescriptions, LdaSimilarity
from analytics.models import Rating

# 1. Kiểm tra bảng ratings
print("=" * 60)
print("1. KIỂM TRA BẢNG RATINGS")
print("=" * 60)
total_ratings = Rating.objects.count()
print(f"Tổng số ratings: {total_ratings}")

user_400003_ratings = Rating.objects.filter(user_id='400001')
print(f"User 400003 có {user_400003_ratings.count()} ratings")

if user_400003_ratings.count() > 0:
    print("\nDanh sách phim user 400003 đã đánh giá:")
    for rating in user_400003_ratings[:10]:  # Hiển thị 10 cái đầu
        print(f"  - Movie ID: {rating.movie_id}, Rating: {rating.rating}")
    if user_400003_ratings.count() > 10:
        print(f"  ... và {user_400003_ratings.count() - 10} ratings khác")

# 2. Kiểm tra bảng lda_similarity
print("\n" + "=" * 60)
print("2. KIỂM TRA BẢNG LDA_SIMILARITY")
print("=" * 60)
total_similarities = LdaSimilarity.objects.count()
print(f"Tổng số similarities: {total_similarities}")

if user_400003_ratings.count() > 0:
    print("\nKiểm tra phim user 400003 đã đánh giá có trong lda_similarity không:")
    found_count = 0
    for rating in user_400003_ratings[:100]:  # Kiểm tra 5 cái đầu
        movie_id = str(rating.movie_id)
        sim_count = LdaSimilarity.objects.filter(source=movie_id).count()
        print(f"  - Movie ID {movie_id}: {sim_count} similarities")
        if sim_count > 0:
            found_count += 1
            # Hiển thị 3 phim tương tự đầu tiên
            sims = LdaSimilarity.objects.filter(source=movie_id)[:3]
            for sim in sims:
                print(f"      → Similar to: {sim.target} (sim: {sim.similarity})")
    
    print(f"\nSummary: {found_count}/5 phim được kiểm tra có similarities")

# 3. Kiểm tra bảng movie_description
print("\n" + "=" * 60)
print("3. KIỂM TRA BẢNG MOVIE_DESCRIPTION")
print("=" * 60)
total_descriptions = MovieDescriptions.objects.count()
print(f"Tổng số movie descriptions: {total_descriptions}")
