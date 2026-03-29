<script lang="ts">
    import type { ListSchema } from "$api-client";
    import type { IStat } from "../../types";
    import Stats from "./Stats.svelte";

    interface ListStatsProps {
        lists: ListSchema[];
    }
    const { lists }: ListStatsProps = $props();
    const listStats = $derived([
        {
            title: "Total Lists",
            value: lists.length,
            description: `of ${lists.length} total`,
            icon: "list",
        },
        {
            title: "Total Entries",
            value: lists.reduce((sum, list) => sum + list.totalEntries, 0),
            description: `across all lists`,
            icon: "check-square",
        },
    ]);
    const completionStats = $derived([
        {
            title: "Completed",
            value: lists.reduce((sum, list) => sum + list.completedEntries, 0),
            description: `items finished`,
            icon: "check-circle",
        },
        {
            title: "Pending",
            value: lists.reduce((sum, list) => sum + list.pendingEntries, 0),
            description: `items remaining`,
            icon: "circle",
        },
    ]);
</script>

<div class="flex flex-col md:flex-row gap-6 w-full justify-center">
    <Stats objects={listStats} />
    <Stats objects={completionStats} />
</div>
