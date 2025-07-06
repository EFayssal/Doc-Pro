document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('download-pdf-btn');
    if (!btn) return;
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        // Masquer les éléments no-print avant export
        document.querySelectorAll('.no-print').forEach(el => el.style.display = 'none');
        // Générer le PDF
        const element = document.querySelector('.page-a3');
        const opt = {
            margin:       0,
            filename:     'cv_modern.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'mm', format: 'a3', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save().then(() => {
            // Réafficher les éléments no-print après export
            document.querySelectorAll('.no-print').forEach(el => el.style.display = '');
        });
    });
});
