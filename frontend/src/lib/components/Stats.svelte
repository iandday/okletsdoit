<script lang="ts">
    import type { IStat } from "../../types";

    interface StatsProps {
        objects: IStat[];
    }

    let { objects }: StatsProps = $props();
</script>

<div class="stats shadow mt-8">
    {#each objects as obj, index (index)}
        <div class="stat bg-accent border-accent-content/20 text-accent-content">
            {#if obj.icon}
                <div class="stat-figure text-primary">
                    <span class="icon-[lucide--{obj.icon}] size-8"></span>
                </div>
            {/if}
            <div class="stat-title text-accent-content">{obj.title}</div>
            <div class="stat-value text-accent-content">{obj.value}</div>
            {#if obj.description}
                <div class="stat-desc text-accent-content">{obj.description}</div>
            {/if}
        </div>
    {/each}
</div>
