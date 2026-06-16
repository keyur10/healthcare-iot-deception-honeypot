document.addEventListener('DOMContentLoaded', () => {
    
    const saveButtons = document.querySelectorAll('.save-btn');

    saveButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault(); // Stop page from refreshing immediately

            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            this.style.opacity = '0.7';
            this.disabled = true;

            setTimeout(() => {
                // Show success checkmark
                this.innerHTML = '<i class="fas fa-check"></i> Saved';
                this.style.background = '#00ff88'; // Turn green
                this.style.color = '#000';

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = '';
                    this.style.color = '';
                    this.style.opacity = '1';
                    this.disabled = false;
                }, 2000);

            }, 1500);
        });
    });
});