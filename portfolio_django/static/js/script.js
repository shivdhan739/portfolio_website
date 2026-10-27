
document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // 1. Automatically update the copyright year.
    const yearElement = document.getElementById("current-year");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // 2. Close the mobile navigation after clicking a link.
    const navbar = document.getElementById("mainNavbar");
    const navLinks = document.querySelectorAll("#mainNavbar .nav-link, #mainNavbar .btn");

    if (navbar && typeof bootstrap !== "undefined") {
        navLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                if (
                    window.innerWidth < 992 &&
                    navbar.classList.contains("show")
                ) {
                    const collapse = bootstrap.Collapse.getOrCreateInstance(navbar);
                    collapse.hide();
                }
            });
        });
    }

    // 3. Contact form character counter.
    const messageField = document.getElementById("message");
    const messageCount = document.getElementById("messageCount");

    if (messageField && messageCount) {
        const maxLength = Number(messageField.getAttribute("maxlength")) || 2000;

        function updateMessageCounter() {
            const currentLength = messageField.value.length;
            messageCount.textContent = currentLength;
            messageCount.parentElement.classList.toggle(
                "text-danger",
                currentLength >= maxLength
            );
        }

        messageField.addEventListener("input", updateMessageCounter);
        updateMessageCounter();
    }

    // 4. Contact form validation + protection against double submit.
    const contactForm = document.getElementById("contactForm");
    const submitButton = document.getElementById("contactSubmit");

    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            if (!contactForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                contactForm.classList.add("was-validated");
                return;
            }

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = "Sending...";
            }
        });
    }

    // 5. Smooth scrolling for links that point to page sections.
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: window.matchMedia(
                        "(prefers-reduced-motion: reduce)"
                    ).matches ? "auto" : "smooth",
                    block: "start"
                });
            }
        });
    });

    // 6. Add a subtle shadow when the header is scrolled.
    const siteHeader = document.querySelector(".site-header");

    function updateHeader() {
        if (siteHeader) {
            siteHeader.classList.toggle("scrolled", window.scrollY > 20);
        }
    }

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    // 7. Reveal animated elements when they enter the viewport.
    const revealElements = document.querySelectorAll(".reveal-on-scroll");

    if ("IntersectionObserver" in window && revealElements.length > 0) {
        const observer = new IntersectionObserver(
            function (entries, currentObserver) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach(function (element) {
            observer.observe(element);
        });
    } else {
        revealElements.forEach(function (element) {
            element.classList.add("is-visible");
        });
    }
});
