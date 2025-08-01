document.addEventListener('DOMContentLoaded', () => {
    // Animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // Carousel Logic
    const track = document.querySelector('.carousel-track');
    if (track) {
        const slides = Array.from(track.children);
        const nextButton = document.querySelector('#nextBtn');
        const prevButton = document.querySelector('#prevBtn');
        let slideWidth = slides.length > 0 ? slides[0].getBoundingClientRect().width : 0;
        let currentIndex = 0;

        const setSlidePosition = (slide, index) => {
            if(slideWidth > 0) {
               slide.style.left = slideWidth * index + 'px';
            }
        };
        slides.forEach(setSlidePosition);

        const updateCarousel = () => {
            if(slideWidth > 0) {
                const amountToMove = currentIndex * slideWidth;
                track.style.transform = 'translateX(-' + amountToMove + 'px)';
            }
        };

        nextButton.addEventListener('click', e => {
            currentIndex = (currentIndex + 1) % slides.length;
            updateCarousel();
        });

        prevButton.addEventListener('click', e => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateCarousel();
        });
        
        window.addEventListener('resize', () => {
            slideWidth = slides.length > 0 ? slides[0].getBoundingClientRect().width : 0;
             slides.forEach((slide, index) => {
               slide.style.left = slideWidth * index + 'px';
            });
            updateCarousel();
        });
    }

    // --- FORM MODAL SCRIPT ---
    const modal = document.getElementById('form-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const openModalBtns = document.querySelectorAll('.open-form-btn');
    const contactForm = document.getElementById('contact-form');
    const paqueteInput = document.getElementById('paquete');

    // Open modal
    openModalBtns.forEach(button => {
        button.addEventListener('click', () => {
            const paqueteNombre = button.getAttribute('data-paquete');
            paqueteInput.value = paqueteNombre;
            modal.classList.add('visible');
        });
    });

    // Close modal function
    const closeModal = () => {
        modal.classList.remove('visible');
    };

    // Close modal events
    closeModalBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    });

    // Form submission
    contactForm.addEventListener('submit', (event) => {
        event.preventDefault(); 
        
        const submitButton = contactForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Enviando...';

        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData.entries());

        // Usamos fetch para enviar los datos al backend de Flask
        fetch('/enviar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                alert('¡Gracias! Tu solicitud ha sido enviada con éxito. Te contactaremos pronto.');
                contactForm.reset();
                closeModal();
            } else {
                alert('Error: ' + result.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error de conexión. Por favor, intenta de nuevo.');
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Enviar Solicitud';
        });
    });
});