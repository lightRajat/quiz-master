<script setup>
    import { Toast } from 'bootstrap';
    import { reactive, onMounted } from 'vue';

    const toast = reactive({
        head: '',
        body: '',
        instance: null
    });

    onMounted(() => {
        const toastElem = document.getElementById('toast');
        toast.instance = new Toast(toastElem);
    });

    window.showToast = (head, body) => {
        toast.head = head;
        toast.body = body;
        toast.instance.show();
    };
</script>

<template>
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <img src="..." class="rounded me-2" alt="...">
                <strong ref="toastHeader" class="me-auto">{{ toast.head }}</strong>
                <small>11 mins ago</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div ref="toastBody" class="toast-body">
                {{ toast.body }}
            </div>
        </div>
    </div>
</template>