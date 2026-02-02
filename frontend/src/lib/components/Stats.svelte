<script lang="ts">
    import type { IStat } from "../../types";

    interface StatsProps {
        objects: IStat[];
        /**
         * Layout direction: 'horizontal' or 'vertical'
         * @default 'horizontal'
         */
        layout?: "horizontal" | "vertical";
        /**
         * Size of the stats component
         * @default 'md'
         */
        size?: "sm" | "md" | "lg";
        /**
         * Text alignment for stat content
         * @default 'left'
         */
        align?: "left" | "center" | "right";
        /**
         * Additional CSS classes to apply to the container
         */
        class?: string;
    }

    let { objects, layout = "horizontal", size = "md", align = "left", class: className = "" }: StatsProps = $props();

    const layoutClass = $derived(layout === "vertical" ? "stats-vertical" : "stats-horizontal");
    const sizeClasses = $derived({
        sm: "text-sm",
        md: "",
        lg: "text-lg",
    });
    const alignClass = $derived(
        {
            left: "text-left",
            center: "text-center",
            right: "text-right",
        }[align],
    );
</script>

<div class="stats shadow mt-8 {layoutClass} {sizeClasses[size]} {className}">
    {#each objects as obj, index (index)}
        <div class="stat bg-accent border-accent-content/20 text-accent-content {alignClass}">
            {#if obj.icon}
                <div class="stat-figure text-primary">
                    <span
                        class="icon-[lucide--{obj.icon}] {size === 'sm'
                            ? 'size-6'
                            : size === 'lg'
                              ? 'size-10'
                              : 'size-8'}"></span>
                </div>
            {/if}
            <div class="stat-title text-accent-content">{obj.title}</div>
            <div class="stat-value text-accent-content {size === 'sm' ? 'text-2xl' : size === 'lg' ? 'text-5xl' : ''}">
                {obj.value}
            </div>
            {#if obj.description}
                <div class="stat-desc text-accent-content">{obj.description}</div>
            {/if}
        </div>
    {/each}
</div>
