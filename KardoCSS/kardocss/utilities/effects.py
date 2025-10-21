"""
KardoCSS - Effects and Transitions Utilities
Efectos visuales, sombras, transiciones y animaciones
"""

def generate_effects():
    """Genera clases CSS para efectos y transiciones"""
    
    css = """
/* ===================================
   KardoCSS - Effects & Transitions
   =================================== */

/* Shadows */
.shadow-none {
    box-shadow: none;
}

.shadow-sm {
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.shadow {
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.shadow-md {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-lg {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.shadow-xl {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.shadow-2xl {
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.shadow-inner {
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}

/* Hover Shadows */
.hover\\:shadow-sm:hover {
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.hover\\:shadow:hover {
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.hover\\:shadow-md:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.hover\\:shadow-lg:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.hover\\:shadow-xl:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Transitions */
.transition {
    transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

.transition-all {
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

.transition-colors {
    transition-property: background-color, border-color, color, fill, stroke;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

.transition-opacity {
    transition-property: opacity;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

.transition-shadow {
    transition-property: box-shadow;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

.transition-transform {
    transition-property: transform;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
}

/* Duration */
.duration-75 {
    transition-duration: 75ms;
}

.duration-100 {
    transition-duration: 100ms;
}

.duration-150 {
    transition-duration: 150ms;
}

.duration-200 {
    transition-duration: 200ms;
}

.duration-300 {
    transition-duration: 300ms;
}

.duration-500 {
    transition-duration: 500ms;
}

.duration-700 {
    transition-duration: 700ms;
}

.duration-1000 {
    transition-duration: 1000ms;
}

/* Timing Functions */
.ease-linear {
    transition-timing-function: linear;
}

.ease-in {
    transition-timing-function: cubic-bezier(0.4, 0, 1, 1);
}

.ease-out {
    transition-timing-function: cubic-bezier(0, 0, 0.2, 1);
}

.ease-in-out {
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Transforms */
.transform {
    transform: translateX(var(--tw-translate-x, 0)) translateY(var(--tw-translate-y, 0)) rotate(var(--tw-rotate, 0)) skewX(var(--tw-skew-x, 0)) skewY(var(--tw-skew-y, 0)) scaleX(var(--tw-scale-x, 1)) scaleY(var(--tw-scale-y, 1));
}

.scale-0 {
    --tw-scale-x: 0;
    --tw-scale-y: 0;
}

.scale-50 {
    --tw-scale-x: 0.5;
    --tw-scale-y: 0.5;
}

.scale-75 {
    --tw-scale-x: 0.75;
    --tw-scale-y: 0.75;
}

.scale-90 {
    --tw-scale-x: 0.9;
    --tw-scale-y: 0.9;
}

.scale-95 {
    --tw-scale-x: 0.95;
    --tw-scale-y: 0.95;
}

.scale-100 {
    --tw-scale-x: 1;
    --tw-scale-y: 1;
}

.scale-105 {
    --tw-scale-x: 1.05;
    --tw-scale-y: 1.05;
}

.scale-110 {
    --tw-scale-x: 1.1;
    --tw-scale-y: 1.1;
}

.scale-125 {
    --tw-scale-x: 1.25;
    --tw-scale-y: 1.25;
}

.scale-150 {
    --tw-scale-x: 1.5;
    --tw-scale-y: 1.5;
}

/* Hover Transforms */
.hover\\:scale-105:hover {
    --tw-scale-x: 1.05;
    --tw-scale-y: 1.05;
}

.hover\\:scale-110:hover {
    --tw-scale-x: 1.1;
    --tw-scale-y: 1.1;
}

.hover\\:-translate-y-1:hover {
    --tw-translate-y: -0.25rem;
}

.hover\\:-translate-y-2:hover {
    --tw-translate-y: -0.5rem;
}

.hover\\:-translate-y-3:hover {
    --tw-translate-y: -0.75rem;
}

/* Rotate */
.rotate-0 {
    --tw-rotate: 0deg;
}

.rotate-45 {
    --tw-rotate: 45deg;
}

.rotate-90 {
    --tw-rotate: 90deg;
}

.rotate-180 {
    --tw-rotate: 180deg;
}

.-rotate-45 {
    --tw-rotate: -45deg;
}

.-rotate-90 {
    --tw-rotate: -90deg;
}

.-rotate-180 {
    --tw-rotate: -180deg;
}

/* Opacity */
.opacity-0 {
    opacity: 0;
}

.opacity-25 {
    opacity: 0.25;
}

.opacity-50 {
    opacity: 0.5;
}

.opacity-75 {
    opacity: 0.75;
}

.opacity-80 {
    opacity: 0.8;
}

.opacity-90 {
    opacity: 0.9;
}

.opacity-95 {
    opacity: 0.95;
}

.opacity-100 {
    opacity: 1;
}

/* Hover Opacity */
.hover\\:opacity-50:hover {
    opacity: 0.5;
}

.hover\\:opacity-75:hover {
    opacity: 0.75;
}

.hover\\:opacity-80:hover {
    opacity: 0.8;
}

.hover\\:opacity-90:hover {
    opacity: 0.9;
}

.hover\\:opacity-100:hover {
    opacity: 1;
}

/* Blur */
.blur-none {
    filter: blur(0);
}

.blur-sm {
    filter: blur(4px);
}

.blur {
    filter: blur(8px);
}

.blur-md {
    filter: blur(12px);
}

.blur-lg {
    filter: blur(16px);
}

.blur-xl {
    filter: blur(24px);
}

/* Backdrop Blur */
.backdrop-blur-none {
    backdrop-filter: blur(0);
}

.backdrop-blur-sm {
    backdrop-filter: blur(4px);
}

.backdrop-blur {
    backdrop-filter: blur(8px);
}

.backdrop-blur-md {
    backdrop-filter: blur(12px);
}

.backdrop-blur-lg {
    backdrop-filter: blur(16px);
}

.backdrop-blur-xl {
    backdrop-filter: blur(24px);
}

/* Animations */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes ping {
    75%, 100% {
        transform: scale(2);
        opacity: 0;
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(-25%);
        animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    }
    50% {
        transform: translateY(0);
        animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    }
}

@keyframes fade-in {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slide-in-up {
    from {
        transform: translateY(100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes slide-in-down {
    from {
        transform: translateY(-100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.animate-spin {
    animation: spin 1s linear infinite;
}

.animate-ping {
    animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-bounce {
    animation: bounce 1s infinite;
}

.animate-fade-in {
    animation: fade-in 0.5s ease-out;
}

.animate-slide-in-up {
    animation: slide-in-up 0.5s ease-out;
}

.animate-slide-in-down {
    animation: slide-in-down 0.5s ease-out;
}

/* Cursor */
.cursor-auto {
    cursor: auto;
}

.cursor-default {
    cursor: default;
}

.cursor-pointer {
    cursor: pointer;
}

.cursor-wait {
    cursor: wait;
}

.cursor-text {
    cursor: text;
}

.cursor-move {
    cursor: move;
}

.cursor-not-allowed {
    cursor: not-allowed;
}

/* User Select */
.select-none {
    user-select: none;
}

.select-text {
    user-select: text;
}

.select-all {
    user-select: all;
}

.select-auto {
    user-select: auto;
}

/* Pointer Events */
.pointer-events-none {
    pointer-events: none;
}

.pointer-events-auto {
    pointer-events: auto;
}
"""
    
    return css

