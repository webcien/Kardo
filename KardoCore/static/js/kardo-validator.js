/**
 * KardoValidator - Sistema de validación de formularios para KardoCore
 * Validación en tiempo real con feedback visual
 */

class KardoValidator {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.options = {
            realtime: true,
            showErrors: true,
            errorClass: 'k-input-error',
            successClass: 'k-input-success',
            ...options
        };
        
        this.rules = {};
        this.errors = {};
        this.init();
    }
    
    init() {
        // Prevenir submit por defecto
        this.form.addEventListener('submit', (e) => {
            if (!this.validateAll()) {
                e.preventDefault();
                return false;
            }
        });
        
        // Validación en tiempo real si está habilitada
        if (this.options.realtime) {
            this.form.querySelectorAll('input, textarea, select').forEach(field => {
                field.addEventListener('blur', () => this.validateField(field));
                field.addEventListener('input', () => {
                    if (this.errors[field.name]) {
                        this.validateField(field);
                    }
                });
            });
        }
    }
    
    addRule(fieldName, rules) {
        this.rules[fieldName] = rules;
        return this;
    }
    
    validateField(field) {
        const fieldName = field.name;
        const value = field.value.trim();
        const rules = this.rules[fieldName];
        
        if (!rules) return true;
        
        // Limpiar error anterior
        delete this.errors[fieldName];
        this.clearFieldError(field);
        
        // Aplicar reglas
        for (const [ruleName, ruleValue] of Object.entries(rules)) {
            const validator = this.validators[ruleName];
            if (validator && !validator.call(this, value, ruleValue, field)) {
                this.errors[fieldName] = this.getErrorMessage(ruleName, ruleValue, field);
                this.showFieldError(field, this.errors[fieldName]);
                return false;
            }
        }
        
        // Campo válido
        this.showFieldSuccess(field);
        return true;
    }
    
    validateAll() {
        let isValid = true;
        this.errors = {};
        
        Object.keys(this.rules).forEach(fieldName => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field && !this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    showFieldError(field, message) {
        field.classList.add(this.options.errorClass);
        field.classList.remove(this.options.successClass);
        
        if (this.options.showErrors) {
            let errorDiv = field.parentElement.querySelector('.k-error-message');
            if (!errorDiv) {
                errorDiv = document.createElement('div');
                errorDiv.className = 'k-error-message';
                field.parentElement.appendChild(errorDiv);
            }
            errorDiv.textContent = message;
        }
    }
    
    showFieldSuccess(field) {
        field.classList.remove(this.options.errorClass);
        field.classList.add(this.options.successClass);
        this.clearFieldError(field);
    }
    
    clearFieldError(field) {
        field.classList.remove(this.options.errorClass, this.options.successClass);
        const errorDiv = field.parentElement.querySelector('.k-error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    getErrorMessage(ruleName, ruleValue, field) {
        const messages = {
            required: 'Este campo es obligatorio',
            email: 'Ingresa un email válido',
            minLength: `Mínimo ${ruleValue} caracteres`,
            maxLength: `Máximo ${ruleValue} caracteres`,
            min: `El valor mínimo es ${ruleValue}`,
            max: `El valor máximo es ${ruleValue}`,
            pattern: 'El formato no es válido',
            match: 'Los campos no coinciden',
            url: 'Ingresa una URL válida',
            number: 'Ingresa un número válido',
            integer: 'Ingresa un número entero',
            alpha: 'Solo se permiten letras',
            alphanumeric: 'Solo se permiten letras y números'
        };
        
        return messages[ruleName] || 'Campo inválido';
    }
    
    validators = {
        required(value) {
            return value.length > 0;
        },
        
        email(value) {
            if (!value) return true; // Skip if empty (use required separately)
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(value);
        },
        
        minLength(value, length) {
            return value.length >= length;
        },
        
        maxLength(value, length) {
            return value.length <= length;
        },
        
        min(value, minValue) {
            return parseFloat(value) >= minValue;
        },
        
        max(value, maxValue) {
            return parseFloat(value) <= maxValue;
        },
        
        pattern(value, regex) {
            if (!value) return true;
            return new RegExp(regex).test(value);
        },
        
        match(value, fieldName) {
            const matchField = this.form.querySelector(`[name="${fieldName}"]`);
            return matchField && value === matchField.value;
        },
        
        url(value) {
            if (!value) return true;
            try {
                new URL(value);
                return true;
            } catch {
                return false;
            }
        },
        
        number(value) {
            if (!value) return true;
            return !isNaN(parseFloat(value)) && isFinite(value);
        },
        
        integer(value) {
            if (!value) return true;
            return Number.isInteger(parseFloat(value));
        },
        
        alpha(value) {
            if (!value) return true;
            return /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(value);
        },
        
        alphanumeric(value) {
            if (!value) return true;
            return /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$/.test(value);
        }
    };
    
    getErrors() {
        return this.errors;
    }
    
    reset() {
        this.errors = {};
        this.form.querySelectorAll('input, textarea, select').forEach(field => {
            this.clearFieldError(field);
        });
    }
}

// Auto-inicializar formularios con atributo data-validate
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-validate]').forEach(form => {
        const validator = new KardoValidator(form);
        
        // Leer reglas desde atributos data-*
        form.querySelectorAll('[data-rules]').forEach(field => {
            try {
                const rules = JSON.parse(field.getAttribute('data-rules'));
                validator.addRule(field.name, rules);
            } catch (e) {
                console.error('Error parsing validation rules:', e);
            }
        });
        
        // Guardar referencia al validator en el form
        form.kardoValidator = validator;
    });
});

