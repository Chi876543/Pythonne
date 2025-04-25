// const testCart = {
//     "user_id": 1,
//     "address": "123 đường ABC",
//     "cart": [
//         {
//             "book_id": 5,
//             "quantity": 2,
//             "price": 50000
//         },
//         {
//             "book_id": 2,
//             "quantity": 1,
//             "price": 75000
//         },
//         {
//             "book_id": 3,
//             "quantity": 1,
//             "price": 75000
//         },
//         {
//             "book_id": 4,
//             "quantity": 1,
//             "price": 75000
//         }
//     ]
// }
// const testUser = {
//     id: "1",
//     username: "nguyenvana",
//     password: "12345678",
//     role: "customer",
//     full_name: "Nguyễn Văn A",
//     address: "123 Đường ABC, Quận 1, TP.HCM",
//     email: "nguyenvana@example.com",
//     phone: "0901234567",
//     status: "active"
// };
// localStorage.setItem('cart', JSON.stringify(testCart))
const cart = JSON.parse(localStorage.getItem('cart')) || ''
const user = JSON.parse(localStorage.getItem('user')) || ''
console.log(cart)
let order

let books = []

async function fetchBooks() {
    try {
        const res = await fetch('/api/get_book/', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });
        const text = await res.text();
        books = JSON.parse(text);
        console.log('Danh sách sách', books);
        renderCart();
    } catch (err) {
        console.error('Lỗi:', err);
    }
}
fetchBooks()

// Format số tiền
function formatPrice(price) {
    return price.toLocaleString('vi-VN') + '₫';
}

// Render giỏ hàng
function renderCart() {
    const tbody = document.getElementById('cart-items');
    tbody.innerHTML = ''; // Xóa nội dung cũ
    cart.items.forEach(item => {
        books.forEach(book => {
            if (item.book_id == book.id) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="checkbox"><input type="checkbox" class="item-checkbox"></td>
                    <td class="product">
                        <div class="product-info">
                            <img src="${book.imagePath}" alt="${book.title}">
                            <div>
                                <p>${book.title}</p>
                                <p class="description">ID: ${book.id}</p>
                                <p> Tác giả: ${book.author}</p>
                            </div>
                        </div>
                    </td>
                    <td class="price" data-price="${item.price}">${formatPrice(item.price)}</td>
                    <td class="quantity">
                        <button onclick="changeQuantity(this, -1)">-</button>
                        <input type="number" value="${item.quantity}" min="1" oninput="updateQuantity(this)">
                        <button onclick="changeQuantity(this, 1)">+</button>
                    </td>
                    <td class="total">${formatPrice(item.price * item.quantity)}</td>
                `;
                tbody.appendChild(row);
            }
        })
    });
    // Gắn sự kiện sau khi render
    attachEventListeners();
    updateTotalAmount();
}

// Cập nhật thành tiền của một sản phẩm
function updateItemTotal(row) {
    const price = parseInt(row.querySelector('.price').dataset.price);
    const quantity = parseInt(row.querySelector('.quantity input').value);
    const total = price * quantity;
    row.querySelector('.total').textContent = formatPrice(total);
    updateTotalAmount();
}

// Cập nhật tổng thanh toán
function updateTotalAmount() {
    let total = 0;
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        const row = checkbox.closest('tr');
        const price = parseInt(row.querySelector('.price').dataset.price);
        const quantity = parseInt(row.querySelector('.quantity input').value);
        total += price * quantity;
    });
    document.getElementById('total-amount').textContent = formatPrice(total);
}

// Xử lý nút tăng/giảm số lượng
function changeQuantity(button, delta) {
    const input = button.parentElement.querySelector('input');
    let value = parseInt(input.value);
    value = Math.max(1, value + delta);
    input.value = value;
    updateItemTotal(button.closest('tr'));
}

// Xử lý nhập số lượng trực tiếp
function updateQuantity(input) {
    let value = parseInt(input.value);
    if (value < 1 || isNaN(value)) {
        input.value = 1;
    }
    updateItemTotal(input.closest('tr'));
}

// Gắn sự kiện cho checkbox
function attachEventListeners() {
    // Chọn tất cả
    document.getElementById('select-all').addEventListener('change', function () {
        document.querySelectorAll('.item-checkbox').forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        updateTotalAmount();
    });

    // Chọn từng sản phẩm
    document.querySelectorAll('.item-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            if (!this.checked) {
                document.getElementById('select-all').checked = false;
            }
            updateTotalAmount();
        });
    });
}


// Mở modal thanh toán
function openCheckoutModal() {
    const checkedItems = document.querySelectorAll('.item-checkbox:checked');
    if (checkedItems.length === 0) {
        alert('Vui lòng chọn ít nhất một sản phẩm để thanh toán!');
        return;
    }
    const modal = document.getElementById('checkout-modal');
    const addressInput = document.getElementById('address');
    addressInput.value = user.address;
    modal.style.display = 'flex';
}

// Đóng modal
function closeModal() {
    document.getElementById('checkout-modal').style.display = 'none';
    document.getElementById('summary-modal').style.display = 'none';
}

// Hiển thị tóm tắt hóa đơn
function showOrderSummary() {
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const note = document.getElementById('note').value;

    if (!name || !address || !phone) {
        alert('Vui lòng nhập đầy đủ họ và tên, địa chỉ và số điện thoại!');
        return;
    }

    const summaryItems = document.getElementById('summary-items');
    summaryItems.innerHTML = '';
    let total = 0;
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        const row = checkbox.closest('tr');
        const title = row.querySelector('.product p').textContent;
        const price = parseInt(row.querySelector('.price').dataset.price);
        const quantity = parseInt(row.querySelector('.quantity input').value);
        const itemTotal = price * quantity;
        total += itemTotal;

        const itemDiv = document.createElement('div');
        itemDiv.className = 'summary-item';
        itemDiv.innerHTML = `
            <span>${title} (x${quantity})</span>
            <span>${formatPrice(itemTotal)}</span>
        `;
        summaryItems.appendChild(itemDiv);
    });

    // Kiểm tra sự tồn tại của các phần tử trước khi gán
    const summaryTotal = document.getElementById('summary-total');
    const summaryAddress = document.getElementById('summary-address');
    const summaryName = document.getElementById('summary-name');
    const summaryPhone = document.getElementById('summary-phone');
    const summaryNote = document.getElementById('summary-note');

    if (summaryTotal && summaryAddress && summaryName && summaryPhone && summaryNote) {
        summaryTotal.textContent = formatPrice(total);
        summaryAddress.textContent = address;
        summaryName.textContent = name;
        summaryPhone.textContent = phone;
        summaryNote.textContent = note || 'Không có';
    } else {
        console.error('Một hoặc nhiều phần tử tóm tắt không tồn tại.');
        return;
    }

    document.getElementById('checkout-modal').style.display = 'none';
    document.getElementById('summary-modal').style.display = 'flex';
}
// Xử lý đặt hàng và gửi đến API
async function placeOrder() {
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const note = document.getElementById('note').value;

    // Tạo dữ liệu gửi đến API
    const apiData = {
        user_id: user.id,
        address: address,
        cart: []
    };

    let total_amount = 0;
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        const row = checkbox.closest('tr');
        const book_id = parseInt(row.querySelector('.description').textContent.split('ID: ')[1]);
        const price = parseInt(row.querySelector('.price').dataset.price);
        const quantity = parseInt(row.querySelector('.quantity input').value);
        total_amount += price * quantity;

        apiData.cart.push({
            book_id: book_id,
            quantity: quantity,
            price: price
        });
    });

    // Gửi dữ liệu đến API
    try {
        console.log(apiData)
        const response = await fetch('/api/create_order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(apiData)
        });

        const result = await response.json();
        if (response.ok) {
            alert(`Đặt hàng thành công! Mã đơn hàng: ${result.order_id}`);
            closeModal();
        } else {
            alert(`Lỗi: ${result.error}`);
        }
    } catch (error) {
        console.error('Lỗi khi gửi đơn hàng:', error);
        alert('Đã có lỗi xảy ra. Vui lòng thử lại.');
    }
}