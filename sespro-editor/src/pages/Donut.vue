<script>
    import {Doughnut} from "vue-chartjs";

    export default {
        name: "Donut",
        extends: Doughnut,
        props: {
            data: Object,
            options: Object
        },
        mounted() {
            this.renderChart(this.data, this.options);
        }
    }
</script>
