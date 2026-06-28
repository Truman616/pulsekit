document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Mobile Navigation Drawer Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNav = document.querySelector('.mobile-nav');

    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileNav.classList.toggle('open');
            const icon = mobileMenuBtn.querySelector('i');
            if (mobileNav.classList.contains('open')) {
                icon.setAttribute('data-lucide', 'x');
            } else {
                icon.setAttribute('data-lucide', 'menu');
            }
            lucide.createIcons(); // Re-render icon change
        });
    }

    // Code Library Tab Switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Deactivate all tabs
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Activate chosen tab
            btn.classList.add('active');
            const targetEl = document.getElementById(`tab-${targetTab}`);
            if (targetEl) {
                targetEl.classList.add('active');
            }
        });
    });

    // Copy to Clipboard Functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const targetId = btn.getAttribute('data-target');
            const codeEl = document.getElementById(targetId);
            if (!codeEl) return;

            const codeText = codeEl.textContent;

            try {
                await navigator.clipboard.writeText(codeText);
                
                // Visual feedback
                btn.classList.add('copied');
                const btnSpan = btn.querySelector('span');
                const btnIcon = btn.querySelector('i');
                
                if (btnSpan) btnSpan.textContent = 'Copied!';
                if (btnIcon) {
                    btnIcon.setAttribute('data-lucide', 'check');
                    lucide.createIcons();
                }

                // Revert after 2 seconds
                setTimeout(() => {
                    btn.classList.remove('copied');
                    if (btnSpan) btnSpan.textContent = 'Copy Code';
                    if (btnIcon) {
                        btnIcon.setAttribute('data-lucide', 'copy');
                        lucide.createIcons();
                    }
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
            }
        });
    });

    // Dynamic Header Shadows on Scroll
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            header.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
            header.style.background = 'rgba(6, 9, 19, 0.9)';
        } else {
            header.style.boxShadow = 'none';
            header.style.background = 'rgba(6, 9, 19, 0.75)';
        }
    });
});
