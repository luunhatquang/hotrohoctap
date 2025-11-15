// Debug: Kiểm tra xem file có được load không
console.log('student_profile.js đã được load thành công!');

function confirmDelete(deleteUrl, examName) {
    if (confirm('Bạn có chắc chắn muốn xóa điểm ' + examName + ' không?\n\nHành động này không thể hoàn tác!')) {
        window.location.href = deleteUrl;
    }
}

function confirmDeleteProfile(deleteUrl) {
    console.log('confirmDeleteProfile được gọi với URL:', deleteUrl);
    
    var confirmation = confirm('⚠️ CẢNH BÁO NGHIÊM TRỌNG ⚠️\n\n' +
        'Bạn có chắc chắn muốn XÓA TOÀN BỘ HỒ SƠ không?\n\n' +
        'Hành động này sẽ xóa:\n' +
        '• Tất cả thông tin cá nhân\n' +
        '• Tất cả điểm thi thử\n' +
        '• Tất cả điểm HSA\n' +
        '• Tất cả điểm TSA\n' +
        '• Toàn bộ dữ liệu hồ sơ\n\n' +
        'HÀNH ĐỘNG NÀY KHÔNG THỂ HOÀN TÁC!\n\n' +
        'Nhấn OK để xác nhận xóa, hoặc Cancel để hủy.');
    
    if (confirmation) {
        var doubleConfirm = confirm('Xác nhận lần cuối!\n\nBạn thực sự muốn xóa toàn bộ hồ sơ?\n\nSau khi xóa, bạn sẽ phải tạo hồ sơ mới từ đầu.');
        if (doubleConfirm) {
            console.log('Đang chuyển hướng đến:', deleteUrl);
            window.location.href = deleteUrl;
        } else {
            console.log('User đã hủy ở bước xác nhận thứ 2');
        }
    } else {
        console.log('User đã hủy ở bước xác nhận đầu tiên');
    }
}

