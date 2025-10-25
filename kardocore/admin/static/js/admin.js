// KardoAdmin JavaScript

// Sidebar toggle for mobile
document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        
        // Close sidebar when clicking outside
        document.addEventListener('click', (e) => {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
});

// Delete user confirmation
async function deleteUser(userId) {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            alert('Usuario eliminado correctamente');
            location.reload();
        } else {
            alert('Error al eliminar usuario');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar usuario');
    }
}

// Delete content confirmation
async function deleteContent(contentId) {
    if (!confirm('¿Estás seguro de eliminar este contenido?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/content/${contentId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            alert('Contenido eliminado correctamente');
            location.reload();
        } else {
            alert('Error al eliminar contenido');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar contenido');
    }
}

// File upload handling
function setupFileUpload() {
    const fileInput = document.getElementById('file-upload');
    if (!fileInput) return;
    
    fileInput.addEventListener('change', async (e) => {
        const files = e.target.files;
        if (!files.length) return;
        
        const formData = new FormData();
        for (const file of files) {
            formData.append('files', file);
        }
        
        try {
            const response = await fetch('/admin/files/upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                alert('Archivos subidos correctamente');
                location.reload();
            } else {
                alert('Error al subir archivos');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al subir archivos');
        }
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload();
});
