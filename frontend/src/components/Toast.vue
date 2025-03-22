<script setup>
    import { Toast } from 'bootstrap';
    import { reactive, onMounted } from 'vue';

    const colorClasses = {
        success: {
            'head': "bg-success text-light",
            'body': "bg-success-subtle text-dark",
            'icon': "bi-check-circle",
            'close': "btn-close-white"
        },
        danger: {
            'head': "bg-danger text-light",
            'body': "bg-danger-subtle text-dark",
            'icon': "bi-x-circle-fill",
            'close': "btn-close-white"
        },
        warning: {
            'head': "bg-warning text-body-secondary",
            'body': "bg-warning-subtle text-dark",
            'icon': "bi-exclamation-triangle-fill",
            'close': "btn-close-dark"
        },
        primary: {
            'head': "bg-primary text-light",
            'body': "bg-primary-subtle text-dark",
            'icon': "bi-info-circle-fill",
            'close': "btn-close-white"
        }
    };

    const toast = reactive({
        head: '',
        body: '',
        instance: null,
        colorClass: colorClasses.success
    });

    onMounted(() => {
        const toastElem = document.getElementById('toast');
        toast.instance = new Toast(toastElem);
    });

    window.showToast = function (head, type = 'success', body = '') {
        toast.head = head;
        toast.body = body;
        toast.colorClass = colorClasses[type];
        toast.instance.show();
    };
</script>

<template>
    <div class="toast-container position-fixed top-0 end-0 p-3">
        <div id="toast" class="toast border-0">
            <div class="toast-header" :class="toast.colorClass.head">
                <i class="bi me-2 fs-5" :class="toast.colorClass.icon"></i>
                <strong class="me-auto fs-5">{{ toast.head }}</strong>
                <button type="button" class="btn-close" :class="toast.colorClass.close" data-bs-dismiss="toast"></button>
            </div>
            <div v-show="toast.body" class="toast-body fs-6" :class="toast.colorClass.body">
                {{ toast.body }}
            </div>
        </div>
    </div>
</template>