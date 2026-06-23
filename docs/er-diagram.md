erDiagram

    USER {
        int id PK
        string username
        string email
        string password
        string bio
        string profile_image
        datetime created_at
    }

    MOVIE {
        int id PK
        string title
        string description
        int release_year
        string poster_url
        datetime created_at
    }

    GENRE {
        int id PK
        string name
    }

    REVIEW {
        int id PK
        int user_id FK
        int movie_id FK
        text content
        int rating
        datetime created_at
        datetime updated_at
    }

    COMMENT {
        int id PK
        int user_id FK
        int review_id FK
        text content
        datetime created_at
    }

    REVIEW_LIKE {
        int id PK
        int user_id FK
        int review_id FK
        datetime created_at
    }

    WATCHLIST {
        int id PK
        int user_id FK
        int movie_id FK
        datetime added_at
    }

    WATCHED_MOVIE {
        int id PK
        int user_id FK
        int movie_id FK
        datetime watched_at
    }

    MOVIE_GENRE {
        int movie_id FK
        int genre_id FK
    }

    USER ||--o{ REVIEW : writes
    MOVIE ||--o{ REVIEW : has

    USER ||--o{ COMMENT : writes
    REVIEW ||--o{ COMMENT : has

    USER ||--o{ REVIEW_LIKE : likes
    REVIEW ||--o{ REVIEW_LIKE : receives

    USER ||--o{ WATCHLIST : adds
    MOVIE ||--o{ WATCHLIST : saved_in

    USER ||--o{ WATCHED_MOVIE : marks
    MOVIE ||--o{ WATCHED_MOVIE : watched

    MOVIE ||--o{ MOVIE_GENRE : belongs_to
    GENRE ||--o{ MOVIE_GENRE : categorizes
