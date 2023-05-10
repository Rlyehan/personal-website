use serde::{Serialize, Deserialize};
use actix_files::Files;
use actix_web::{web, App, HttpServer, error::ResponseError, HttpResponse};
use std::fs;
use std::io::Read;
use std::fmt;

#[derive(Debug, Serialize, Deserialize)]
struct BlogPost {
    id: u32,
    title: String,
    preview: String,
    content: String,
    image_references: Vec<String>,
}

#[derive(Debug, Serialize)]
struct BlogPostSummary {
    id: u32,
    title: String,
    preview: String,
}

#[derive(Debug)]
enum BlogPostError {
    FileOpenError,
    FileReadError,
    ParseError,
    SerializationError,
}

impl fmt::Display for BlogPostError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            BlogPostError::FileOpenError => write!(f, "Unable to open file"),
            BlogPostError::FileReadError => write!(f, "Unable to read file"),
            BlogPostError::ParseError => write!(f, "Unable to parse JSON"),
            BlogPostError::SerializationError => write!(f, "Unable to serialize summaries"),
        }
    }
}

impl ResponseError for BlogPostError {
    fn error_response(&self) -> HttpResponse {
        match *self {
            BlogPostError::FileOpenError => HttpResponse::NotFound().json("Blog post not found"),
            BlogPostError::FileReadError => HttpResponse::InternalServerError().json("Unable to read file"),
            BlogPostError::ParseError => HttpResponse::InternalServerError().json("Unable to parse JSON"),
            BlogPostError::SerializationError => HttpResponse::InternalServerError().json("Unable to serialize summaries"),
        }
    }
}

async fn get_blog_post(id: web::Path<String>) -> Result<String, BlogPostError> {
    let file_path = format!("./blog_post/{}.json", id);
    let mut file = match fs::File::open(&file_path) {
        Ok(file) => file,
        Err(e) => match e.kind() {
            std::io::ErrorKind::NotFound => return Err(BlogPostError::FileOpenError),
            _ => return Err(BlogPostError::FileReadError),
        },
    };
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .map_err(|_| BlogPostError::FileReadError)?;
    Ok(contents)
}


async fn get_blog_post_summaries() -> Result<String, BlogPostError> {
    let mut summaries = Vec::new();

    let entries = fs::read_dir("./blog_post")
        .map_err(|_| BlogPostError::FileReadError)?;

    for entry in entries {
        let entry = entry.map_err(|_| BlogPostError::FileReadError)?;
        if entry.path().extension() == Some(&std::ffi::OsStr::new("json")) {
            let mut file = fs::File::open(entry.path())
                .map_err(|_| BlogPostError::FileOpenError)?;
            let mut contents = String::new();
            file.read_to_string(&mut contents)
                .map_err(|_| BlogPostError::FileReadError)?;

            let post: BlogPost = serde_json::from_str(&contents)
                .map_err(|_| BlogPostError::ParseError)?;
            let summary = BlogPostSummary {
                id: post.id,
                title: post.title,
                preview: post.preview,
            };
            summaries.push(summary);
        }
    }

    serde_json::to_string(&summaries)
        .map_err(|_| BlogPostError::SerializationError)
}


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/blog_post/{id}", web::get().to(get_blog_post))
            .route("blog_posts", web::get().to(get_blog_post_summaries))
            .service(Files::new("/images", "./images"))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}