// static/js/customer/home.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const bookList = document.getElementById('book-list');
    const pagination = document.getElementById('pagination');

    let currentPage = 1;
    let currentQuery = '';

    // Hàm lấy danh sách sách
    function fetchBooks(page = 1, query = '') {
        const url = `/books/?page=${page}&q=${encodeURIComponent(query)}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Cập nhật danh sách sách
                bookList.innerHTML = '';
                if (data.books.length === 0) {
                    bookList.innerHTML = '<p>Không tìm thấy sách nào.</p>';
                } else {
                    data.books.forEach(book => {
                        bookList.innerHTML += `
                            <div class="col-md-3 book-item">
                                <div class="card">
                                    <img src="${book.imagePath || '/static/images/default_book.jpg'}" class="card-img-top" alt="${book.title}">
                                    <div class="card-body">
                                        <h5 class="card-title">${book.title}</h5>
                                        <p class="card-text">Tác giả: ${book.author || 'Không rõ'}</p>
                                        <p class="card-text">Giá: ${book.price} VNĐ</p>
                                        <p class="card-text">Tồn kho: ${book.stock}</p>
                                        <a href="/books/${book.id}/" class="btn btn-info">Xem chi tiết</a>
                                        <a href="/orders/create/?book_id=${book.id}" class="btn btn-success">Đặt hàng ngay</a>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                }

                // Cập nhật phân trang
                pagination.innerHTML = '';
                if (data.has_previous) {
                    pagination.innerHTML += `
                        <li class="page-item">
                            <a class="page-link" href="#" data-page="${data.previous_page}">Trước</a>
                        </li>
                    `;
                }
                pagination.innerHTML += `
                    <li class="page-item disabled">
                        <span class="page-link">Trang ${data.current_page} / ${data.total_pages}</span>
                    </li>
                `;
                if (data.has_next) {
                    pagination.innerHTML += `
                        <li class="page-item">
                            <a class="page-link" href="#" data-page="${data.next_page}">Sau</a>
                        </li>
                    `;
                }

                // Thêm sự kiện cho các nút phân trang
                document.querySelectorAll('.page-link').forEach(link => {
                    link.addEventListener('click', function(e) {
                        e.preventDefault();
                        currentPage = parseInt(this.getAttribute('data-page'));
                        fetchBooks(currentPage, currentQuery);
                    });
                });
            })
            .catch(error => {
                console.error('Error:', error);
                bookList.innerHTML = '<p>Đã có lỗi xảy ra. Vui lòng thử lại.</p>';
            });
    }

    // Sự kiện tìm kiếm
    searchInput.addEventListener('input', function() {
        currentQuery = this.value;
        currentPage = 1;  // Reset về trang 1 khi tìm kiếm
        fetchBooks(currentPage, currentQuery);
    });

    searchButton.addEventListener('click', function(e) {
        e.preventDefault();
        currentQuery = searchInput.value;
        currentPage = 1;
        fetchBooks(currentPage, currentQuery);
    });

    // Lấy danh sách sách ban đầu
    fetchBooks(currentPage, currentQuery);
});