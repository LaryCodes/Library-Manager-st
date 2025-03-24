import json
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd

LIBRARY_FILE = "library.txt"

# Function to load books from file
def load_books():
    try:
        with open(LIBRARY_FILE, "r") as file:
            books = json.load(file)
        return books
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save books to file
def save_books(books):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Set page config
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 28px;
        font-weight: bold;
        color: #2563EB;
        margin-bottom: 15px;
        border-bottom: 2px solid #BFDBFE;
        padding-bottom: 10px;
    }
    .card {
        background-color: #EFF6FF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        border-left: 5px solid #3B82F6;
    }
    .book-title {
        font-weight: bold;
        color: #1E40AF;
        font-size: 18px;
    }
    .book-author {
        color: #3B82F6;
        font-style: italic;
    }
    .book-details {
        color: #475569;
        font-size: 14px;
    }
    .stButton button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #1E40AF;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .read-badge {
        background-color: #10B981;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .unread-badge {
        background-color: #F59E0B;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .stats-card {
        background-color: #DBEAFE;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #1E40AF;
    }
    .stat-label {
        font-size: 16px;
        color: #475569;
    }
    .sidebar .sidebar-content {
        background-color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Load books when the app starts
books = load_books()

# Custom header
st.markdown('<div class="main-header">📚 Personal Library Manager</div>', unsafe_allow_html=True)

# Horizontal menu instead of sidebar
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Add Book", "View All Books", "Search Book", "Remove Book", "Statistics"],
        icons=["plus-circle", "book", "search", "trash", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#DBEAFE", "border-radius": "10px"},
            "icon": {"color": "#2563EB", "font-size": "16px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "padding": "10px", "--hover-color": "#EFF6FF"},
            "nav-link-selected": {"background-color": "#3B82F6", "color": "white", "font-weight": "bold"},
        }
    )

# Add a book
if selected == "Add Book":
    st.markdown('<div class="sub-header">➕ Add a New Book</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")
        year = st.text_input("Publication Year")
    
    with col2:
        genre_options = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Biography", "History", "Self-Help", "Other"]
        genre = st.selectbox("Book Genre", genre_options)
        read_status = st.toggle("I have read this book")
        rating = st.slider("Rating (if read)", 1, 5, 3) if read_status else None
    
    if st.button("Add to Library"):
        if title and author:
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read_status,
                "rating": rating if read_status else None
            }
            books.append(book)
            save_books(books)
            st.balloons()
            st.success("Book added successfully to your library!")
        else:
            st.error("Title and author are required!")

# View all books
elif selected == "View All Books":
    st.markdown('<div class="sub-header">📖 Your Book Collection</div>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.radio("Filter by status:", ["All", "Read", "Unread"])
    with col2:
        if books:
            genres = list(set(book["genre"] for book in books))
            genres.insert(0, "All Genres")
            filter_genre = st.selectbox("Filter by genre:", genres)
        else:
            filter_genre = "All Genres"
    with col3:
        sort_by = st.selectbox("Sort by:", ["Title", "Author", "Year", "Genre"])
    
    # Apply filters
    filtered_books = books.copy()
    if filter_status == "Read":
        filtered_books = [book for book in filtered_books if book["read"]]
    elif filter_status == "Unread":
        filtered_books = [book for book in filtered_books if not book["read"]]
    
    if filter_genre != "All Genres":
        filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]
    
    # Sort books
    sort_key = sort_by.lower()
    filtered_books = sorted(filtered_books, key=lambda x: x[sort_key] if sort_key in x else "")
    
    # Display books
    if filtered_books:
        for book in filtered_books:
            status_badge = '<span class="read-badge">READ</span>' if book["read"] else '<span class="unread-badge">UNREAD</span>'
            rating_stars = "⭐" * book["rating"] if book["read"] and book["rating"] else ""
            
            st.markdown(f"""
            <div class="card">
                <div class="book-title">{book['title']} {status_badge}</div>
                <div class="book-author">by {book['author']}</div>
                <div class="book-details">
                    📅 {book['year']} &nbsp;|&nbsp; 🏷️ {book['genre']} &nbsp;{rating_stars}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No books match your criteria or your library is empty.")

# Search for a book
elif selected == "Search Book":
    st.markdown('<div class="sub-header">🔍 Find Books</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        search_type = st.radio("Search by:", ["Title", "Author", "Genre"])
    with col2:
        keyword = st.text_input("Enter search term:")
    
    if keyword:
        results = [book for book in books if keyword.lower() in book[search_type.lower()].lower()]
        if results:
            st.success(f"Found {len(results)} matching books!")
            for book in results:
                status_badge = '<span class="read-badge">READ</span>' if book["read"] else '<span class="unread-badge">UNREAD</span>'
                rating_stars = "⭐" * book["rating"] if book["read"] and book["rating"] else ""
                
                st.markdown(f"""
                <div class="card">
                    <div class="book-title">{book['title']} {status_badge}</div>
                    <div class="book-author">by {book['author']}</div>
                    <div class="book-details">
                        📅 {book['year']} &nbsp;|&nbsp; 🏷️ {book['genre']} &nbsp;{rating_stars}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"No books found matching '{keyword}' in {search_type}.")

# Remove a book
elif selected == "Remove Book":
    st.markdown('<div class="sub-header">🗑 Remove Books</div>', unsafe_allow_html=True)
    
    if books:
        titles = [book["title"] for book in books]
        book_to_remove = st.selectbox("Select a book to remove:", titles)
        
        # Show book details
        selected_book = next((book for book in books if book["title"] == book_to_remove), None)
        if selected_book:
            status_badge = '<span class="read-badge">READ</span>' if selected_book["read"] else '<span class="unread-badge">UNREAD</span>'
            
            st.markdown(f"""
            <div class="card">
                <div class="book-title">{selected_book['title']} {status_badge}</div>
                <div class="book-author">by {selected_book['author']}</div>
                <div class="book-details">
                    📅 {selected_book['year']} &nbsp;|&nbsp; 🏷️ {selected_book['genre']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            confirm = st.checkbox("I confirm I want to remove this book")
            if confirm and st.button("Remove Book"):
                books = [book for book in books if book["title"] != book_to_remove]
                save_books(books)
                st.success("Book removed successfully!")
    else:
        st.info("No books in the library to remove.")

# Statistics
elif selected == "Statistics":
    st.markdown('<div class="sub-header">📊 Library Statistics</div>', unsafe_allow_html=True)
    
    if books:
        # Basic stats
        total_books = len(books)
        read_books = sum(1 for book in books if book["read"])
        unread_books = total_books - read_books
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        # Create three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stats-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Total Books</div>
            </div>
            """.format(total_books), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="stats-card">
                <div class="stat-number">{}</div>
                <div class="stat-label">Books Read</div>
            </div>
            """.format(read_books), unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="stats-card">
                <div class="stat-number">{:.1f}%</div>
                <div class="stat-label">Completion Rate</div>
            </div>
            """.format(percentage_read), unsafe_allow_html=True)
        
        # Genre distribution
        st.markdown("### 📚 Genre Distribution")
        genre_counts = {}
        for book in books:
            genre = book.get("genre", "Unknown")
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Create DataFrame for plotting
        genre_df = pd.DataFrame({"Genre": list(genre_counts.keys()), "Count": list(genre_counts.values())})
        
        fig = px.pie(genre_df, values="Count", names="Genre", title="Books by Genre",
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        
        # Reading progress over time
        if any(book.get("read") for book in books):
            st.markdown("### 📈 Reading Progress")
            
            # Create a bar chart for read vs unread by genre
            read_by_genre = {}
            unread_by_genre = {}
            
            for book in books:
                genre = book.get("genre", "Unknown")
                if book.get("read"):
                    read_by_genre[genre] = read_by_genre.get(genre, 0) + 1
                else:
                    unread_by_genre[genre] = unread_by_genre.get(genre, 0) + 1
            
            all_genres = set(list(read_by_genre.keys()) + list(unread_by_genre.keys()))
            
            data = []
            for genre in all_genres:
                data.append({"Genre": genre, "Status": "Read", "Count": read_by_genre.get(genre, 0)})
                data.append({"Genre": genre, "Status": "Unread", "Count": unread_by_genre.get(genre, 0)})
            
            progress_df = pd.DataFrame(data)
            
            fig = px.bar(progress_df, x="Genre", y="Count", color="Status", title="Reading Progress by Genre",
                        color_discrete_map={"Read": "#10B981", "Unread": "#F59E0B"})
            fig.update_layout(xaxis_title="Genre", yaxis_title="Number of Books")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some books to view statistics!")
