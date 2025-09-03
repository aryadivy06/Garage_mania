 const twoBtn = document.getElementById('show-twowheelers');
                const fourBtn = document.getElementById('show-fourwheelers');
                const twoDetails = document.getElementById('twowheelers-details');
                const fourDetails = document.getElementById('fourwheelers-details');

                if(twoBtn) {
                    twoBtn.addEventListener('click', () => {
                        twoDetails.style.display = 'block';
                        fourDetails.style.display = 'none';
                        twoBtn.classList.add('active');
                        fourBtn.classList.remove('active');
                    });
                }

                if(fourBtn) {
                    fourBtn.addEventListener('click', () => {
                        twoDetails.style.display = 'none';
                        fourDetails.style.display = 'block';
                        fourBtn.classList.add('active');
                        twoBtn.classList.remove('active');
                    });
                }