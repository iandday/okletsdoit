<script lang="ts">
    import { Chart, PieController, ArcElement, Tooltip, Legend, type ChartConfiguration } from "chart.js";
    import { onMount } from "svelte";

    type PieChartProps = {
        labels: string[];
        data: number[];
        backgroundColor?: string[];
        size?: "sm" | "md" | "lg";
        labelColor?: string;
    };

    const { labels, data, backgroundColor, size = "md", labelColor = "text-base-content" }: PieChartProps = $props();

    let canvasElement: HTMLCanvasElement;
    let chartInstance: Chart | null = null;
    let colorElement: HTMLDivElement;
    let computedColor = $state("#000000");

    // Size configurations
    const sizeMap = {
        sm: { maxWidth: "300px", maxHeight: "300px" },
        md: { maxWidth: "400px", maxHeight: "400px" },
        lg: { maxWidth: "500px", maxHeight: "500px" },
    };

    // Extract color from Tailwind class
    $effect(() => {
        if (colorElement) {
            const style = window.getComputedStyle(colorElement);
            computedColor = style.color;
        }
    });

    // Default color palette
    const defaultColors = [
        "rgba(255, 99, 132, 0.8)",
        "rgba(54, 162, 235, 0.8)",
        "rgba(255, 206, 86, 0.8)",
        "rgba(75, 192, 192, 0.8)",
        "rgba(153, 102, 255, 0.8)",
        "rgba(255, 159, 64, 0.8)",
        "rgba(199, 199, 199, 0.8)",
        "rgba(83, 102, 255, 0.8)",
        "rgba(255, 99, 255, 0.8)",
        "rgba(99, 255, 132, 0.8)",
    ];

    onMount(() => {
        Chart.register(PieController, ArcElement, Tooltip, Legend);

        const config: ChartConfiguration<"pie"> = {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                        backgroundColor: backgroundColor || defaultColors,
                        borderWidth: 2,
                        borderColor: "rgba(0, 0, 0, 0.1)",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            padding: 4,
                            font: {
                                size: 12,
                            },
                            color: computedColor,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const label = context.label || "";
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value.toLocaleString()} (${percentage}%)`;
                            },
                        },
                    },
                },
            },
        };

        chartInstance = new Chart(canvasElement, config);

        return () => {
            chartInstance?.destroy();
        };
    });
</script>

<!-- Hidden element to extract Tailwind color -->
<div bind:this={colorElement} class={labelColor} style="position: absolute; visibility: hidden;"></div>

<div style="max-width: {sizeMap[size].maxWidth}; max-height: {sizeMap[size].maxHeight}; width: 100%;">
    <canvas bind:this={canvasElement}></canvas>
</div>
