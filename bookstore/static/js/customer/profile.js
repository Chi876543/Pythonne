const testUser = {
  id: "1",
  username: "nguyenvana",
  password: "12345678",
  role: "customer",
  full_name: "Nguyễn Văn A",
  address: "123 Đường ABC, Quận 1, TP.HCM",
  email: "nguyenvana@example.com",
  phone: "0901234567",
  status: "active"
};
localStorage.setItem('user', JSON.stringify(testUser))

const cart = localStorage.getItem('cart') || ''
const user = JSON.parse(localStorage.getItem('user')) || ''
let orders = []
const popupOder = document.getElementById('popup-oder');

async function fetchOrders() {
  try {
    const res = await fetch('/api/view_order/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: parseInt(user.id) })
    });
    const text = await res.text();
    orders = JSON.parse(text);
    console.log('Hóa đơn của user:', orders);
    renderOrders(orders);

  } catch (err) {
    console.error('Lỗi:', err);
  }
}

async function fetchSearchOrders(information) {
  try {
    const res = await fetch('/api/search_order/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(information)
    });

    if (!res.ok) {
      throw new Error('Lỗi mạng hoặc server: ' + res.status);
    }

    const data = await res.json();
    console.log('Kết quả tìm kiếm:', data);
    return data;

  } catch (error) {
    console.error('Lỗi khi fetch:', error);
    return [];
  }
}

fetchOrders();

// Hiển thị thông tin người dùng
function loadUserInfor() {
  if (user) {
    document.getElementById("username").textContent = user.username;
    document.getElementById("user-fullname").textContent = user.full_name || "Chưa có";
    document.getElementById("user-sdt").textContent = user.phone || "Chưa có";
    document.getElementById("user-status").textContent = user.status || "Không rõ";
    document.getElementById("user-address").textContent = user.address || "Không rõ";
  } else {
    alert("Bạn chưa đăng nhập! Vui lòng đăng nhập để tiếp tục!");
  }
}

loadUserInfor();

// chuyển đổi từ đơn mua sang tài khoản và ngược lại
document.addEventListener('DOMContentLoaded', () => {
  const profileTab = document.getElementById('profile-tab');
  const orderHistoryTab = document.getElementById('order-history-tab');
  const profileContent = document.getElementById('profile-content');
  const orderContent = document.getElementById('orders-content');

  // Hiển thị nội dung "Tài khoản của tôi"
  profileTab.addEventListener('click', () => {

    orderContent.classList.add('hidden');
    profileContent.classList.remove('hidden');
  });

  // Hiển thị nội dung "Đơn mua"
  orderHistoryTab.addEventListener('click', () => {
    profileContent.classList.add('hidden');
    orderContent.classList.remove('hidden');
  });
});

//nghe sự kiện sửa thông tin người dùng
document.addEventListener('DOMContentLoaded', () => {
  const editButton = document.getElementById('edit-profile-btn');

  let isEditing = false; // Trạng thái chỉnh sửa

  // Sự kiện khi nhấn vào nút "Sửa thông tin"
  editButton.addEventListener('click', () => {
    const userFullname = document.getElementById('user-fullname');
    const userSdt = document.getElementById('user-sdt');
    const userAddress = document.getElementById('user-address');

    if (!isEditing) {
      // Đổi trạng thái sang chỉnh sửa
      isEditing = true;
      editButton.textContent = 'Lưu thông tin';

      // Chuyển các span thành input để chỉnh sửa
      const fullnameInput = document.createElement('input');
      fullnameInput.type = 'text';
      fullnameInput.id = 'edit-fullname';
      fullnameInput.value = userFullname.textContent;
      userFullname.replaceWith(fullnameInput);

      const sdtInput = document.createElement('input');
      sdtInput.type = 'text';
      sdtInput.id = 'edit-sdt';
      sdtInput.value = userSdt.textContent;
      userSdt.replaceWith(sdtInput);

      const addressInput = document.createElement('input');
      addressInput.type = 'text'
      addressInput.id = 'edit-address'
      addressInput.value = userAddress.textContent;
      userAddress.replaceWith(addressInput);

    } else {
      // Đổi trạng thái sang hiển thị
      isEditing = false;
      editButton.textContent = 'Sửa thông tin';

      // Lấy giá trị mới từ input
      const fullnameInput = document.getElementById('edit-fullname');
      const sdtInput = document.getElementById('edit-sdt');
      const addressInput = document.getElementById('edit-address');

      const newFullname = fullnameInput.value.trim();
      const newSdt = sdtInput.value.trim();
      const newAddress = addressInput.value.trim();

      // Tạo lại span và hiển thị thông tin đã sửa
      const updatedFullname = document.createElement('span');
      updatedFullname.id = 'user-fullname';
      updatedFullname.textContent = newFullname;

      const updatedSdt = document.createElement('span');
      updatedSdt.id = 'user-sdt';
      updatedSdt.textContent = newSdt;

      const updateAddress = document.createElement('span');
      updateAddress.id = 'user-address';
      updateAddress.textContent = newAddress;

      fullnameInput.replaceWith(updatedFullname);
      sdtInput.replaceWith(updatedSdt);
      addressInput.replaceWith(updateAddress);

      //Kiểm tra thông tin hợp lệ
      if (newFullname === "") {
        alert('Vui lòng không để trống Họ và tên!');
        loadUserInfor();
        return;
      }
      if (newSdt === "") {
        alert('Số điện thoại không được để trống!');
        loadUserInfor();
        return;
      }
      if (newSdt.length < 10) {
        alert('Số điện thoại không hợp lệ!');
        loadUserInfor();
        return;
      }

      user.fullname = newFullname;
      user.phone = newSdt;
      user.address = newAddress;
      localStorage.setItem('user', JSON.stringify(user));

      alert('Thông tin đã được cập nhật!');
    }
  });
});

function reset() {
  const inputs = document.getElementsByTagName('input');

  for (let input of inputs) {
    input.value = ''; // Đặt giá trị của input về chuỗi rỗng
  }

  const selects = document.getElementsByTagName('select');
  for (let select of selects) {
    select.selectedIndex = 0; // Đặt về tùy chọn đầu tiên
  }
}

function renderOrders(orders) {
  // Hiển thị các hóa đơn trong bảng
  const invoiceTable = document.getElementById('invoice-table').getElementsByTagName('tbody')[0];
  invoiceTable.innerHTML = ''
  if (orders.length == 0) {
    invoiceTable.innerHTML = 'Không tìm thấy hóa đơn!'
  }
  orders.forEach(invoice => {
    const row = document.createElement('tr');

    // ID
    const idCell = document.createElement('td');
    idCell.textContent = invoice.order_id;
    row.appendChild(idCell);

    // Tên
    const dateCell = document.createElement('td');
    dateCell.textContent = user.full_name;
    row.appendChild(dateCell);

    // Ngày
    const totalCell = document.createElement('td');
    totalCell.textContent = invoice.created_at;
    row.appendChild(totalCell);

    //Tổng tiền
    const totalQuantityCell = document.createElement('td');
    totalQuantityCell.textContent = invoice.total_amount + " VNĐ";
    row.appendChild(totalQuantityCell);

    //Địa chỉ
    const addressCell = document.createElement('td');
    addressCell.textContent = invoice.address;
    row.appendChild(addressCell);

    //Trang thái
    const statusCell = document.createElement('td');
    statusCell.textContent = invoice.status;
    row.appendChild(statusCell);

    const detailsCell = document.createElement('td');
    const detailsButton = document.createElement('button');
    detailsButton.textContent = 'Xem chi tiết';
    detailsButton.addEventListener('click', () => showInvoiceDetails(invoice.items));
    detailsCell.appendChild(detailsButton);
    row.appendChild(detailsCell);

    // Thêm dòng vào bảng
    invoiceTable.appendChild(row);
  });
}

//hiển thị chi tiết hóa đơn
function showInvoiceDetails(list) {
  const detailTable = document.getElementById('detail-oder')?.getElementsByTagName('tbody')[0];

  if (!popupOder || !detailTable) {
    console.error("Popup hoặc bảng chi tiết không tồn tại!");
    return;
  }

  // Hiển thị popup
  popupOder.style.display = "flex";

  // Xóa dữ liệu cũ trong bảng chi tiết
  detailTable.innerHTML = '';

  // Thêm dữ liệu mới vào bảng
  list.forEach(detail => {
    const row = document.createElement('tr');

    const productName = document.createElement('td');
    productName.textContent = detail.book_title || 'N/A';
    row.appendChild(productName);

    const quantity = document.createElement('td');
    quantity.textContent = detail.quantity || '0';
    row.appendChild(quantity);

    const unitPrice = document.createElement('td');

    const totalCell = document.createElement('td');
    totalCell.textContent = (detail.total || 0) + "VNĐ";
    row.appendChild(totalCell);

    detailTable.appendChild(row);
  });
}

// Đóng popup
document.getElementById('close-popup').addEventListener('click', () => {
  popupOder.style.display = "none";
  const detailTable = document.getElementById('detail-oder').getElementsByTagName('tbody')[0];
  while (detailTable.rows.length > 0) {
    detailTable.deleteRow(0);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const searchBtn = document.getElementById('search-btn');

  searchBtn.addEventListener('click', async () => {

    const startDate = document.getElementById('search-start-date').value || '';
    const endDate = document.getElementById('search-end-date').value || '';
    const total = document.getElementById('search-total').value || '';
    const address = document.getElementById('search-address').value.trim() || '';
    const status = document.getElementById('search-status').value || '';

    const userId = user.id;

    if (!userId) {
      alert('Không tìm thấy thông tin người dùng!');
      return;
    }

    const information = {
      user_id: userId,
      startDate,
      endDate,
      total,
      address,
      status
    };
    try {
      const response = await fetch('/api/search_order/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(information)
      });

      const data = await response.json();

      if (!response.ok) {
        console.error('Lỗi từ server:', data);
        alert('Lỗi khi tìm kiếm đơn hàng!');
        return;
      }
      console.log('Kết quả tìm kiếm:', data);
      renderOrders(data);

    } catch (error) {
      console.error('Lỗi tìm kiếm:', error);
      alert('Có lỗi xảy ra khi gửi yêu cầu!');
    }
  });
});

function onLogout() {
  localStorage.removeItem('cart');
  localStorage.removeItem('user');
  window.location.href = '/';
}