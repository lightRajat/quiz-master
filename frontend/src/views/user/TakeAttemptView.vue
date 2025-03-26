<script setup>
</script>

<template>
    <main class="container mt-4">
        <!-- heading -->
        <div class="mb-5">
            <h2 class="lead mb-0 ms-1">subject name</h2>
            <h1 class="display-5">Dhapter Name</h1>
        </div>

        <!-- questions -->
        <div class="card">
            <div class="card-body p-4">
                <!-- question -->
                <p class="h5 mb-3">
                    <span class="me-3">1.</span>
                    <span>question</span>
                </p>
                
                <!-- options -->
                <div class="option-grp container mb-2">
                    <div class="row">
                        <input class="col" type="radio" id="option_a" name="option">
                        <label for="option_a" class="radio-label col radio-label-a">
                            <span class="me-2">A.</span>
                            <span>Option 1</span>
                        </label>

                        <input class="col" type="radio" id="option_b" name="option">
                        <label for="option_b" class="radio-label col radio-label-b">
                            <span class="me-2">B.</span>
                            <span>Option 2</span>
                        </label>
                    </div>
                    <div class="row">
                        <input class="col" type="radio" id="option_c" name="option">
                        <label for="option_c" class="radio-label col radio-label-c">
                            <span class="me-2">C.</span>
                            <span>Option 3</span>
                        </label>

                        <input class="col" type="radio" id="option_d" name="option">
                        <label for="option_d" class="radio-label col radio-label-d">
                            <span class="me-2">D.</span>
                            <span>Option 3</span>
                        </label>
                    </div>
                </div>

                <!-- clear option btn -->
                <span class="text-secondary link-underline-secondary clear-btn">Clear Option</span>
            </div>
        </div>
    </main>
    <div class="menu bg-success-subtle">
        <p>will start in 3 seconds</p>
        <p class="fs-4 mb-2">00:00</p>
        <button class="btn btn-success">Sumbit</button>
    </div>
</template>

<style scoped>
.menu {
    position: fixed;
    top: 26px;
    right: 32px;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    opacity: 0.8;
    width: 200px;
}

input[type="radio"] {
    display: none;
}

.radio-label {
    padding: 10px 20px;
    background-color: white;
    cursor: pointer;
    font-size: 16px;
}
.radio-label:hover {
    background-color: #f0f0f0;
}

input[type="radio"]:checked + .radio-label {
    background-color: #198754;
    color: white;
}

.option-grp {
    outline: 1px solid gray;
    border-radius: 6px;
}
.option-grp > .row:first-child {
    border-bottom: 1px solid gray !important;
}
.radio-label-a, .radio-label-c {
    border-right: 1px solid gray !important;
}

.radio-label-a {
    border-top-left-radius: 6px;
}
.radio-label-b {
    border-top-right-radius: 6px;
}
.radio-label-c {
    border-bottom-left-radius: 6px;
}
.radio-label-d {
    border-bottom-right-radius: 6px;
}

.clear-btn:hover {
    text-decoration: underline;
    display: inline-block;
    cursor: pointer;
}
</style>