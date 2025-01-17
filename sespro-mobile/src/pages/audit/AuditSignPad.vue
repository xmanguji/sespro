<template>
    <div class="sign-page">
        <div class="pad-container">
            <div class="headings">Signature Required</div>
            <VueSignaturePad width="100%" height="200px" ref="pad" />
            <b-button @click="$emit('signed')">SUBMIT</b-button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AuditSignPad",
    }
</script>

<style lang="scss" scoped>
    .sign-page {
        width: 100%;
        height: 100%;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .pad-container {
        height: 100%;
        width: 50%;
        background-color: #ffffff;
        border-radius: 2px;
        padding: 0;
        margin: auto;
        overflow-y: scroll;
        display: flex;
        flex-direction: column;
    }

    .headings {
        text-align: center;
        font-weight: 600;
        font-size: 20px;
        margin-top: 4px;
    }
</style>
