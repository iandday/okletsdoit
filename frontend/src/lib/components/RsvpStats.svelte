<script lang="ts">
    import type { RsvpStatsSchema } from "../../../api-client";
    import Stats from "./Stats.svelte";

    interface RsvpStatsProps {
        rsvpStats: RsvpStatsSchema;
        layout?: "horizontal" | "vertical";
    }

    const { rsvpStats, layout = "vertical" }: RsvpStatsProps = $props();
    const responseStats = $derived([
        {
            title: "Attending",
            value: rsvpStats.totalAttending,
            icon: "check-circle",
        },
        {
            title: "Declined",
            value: rsvpStats.totalDeclined,
            icon: "x-circle",
        },
    ]);
</script>

<div class="flex {layout === 'horizontal' ? 'flex-row' : 'flex-col'} gap-6 w-full justify-center">
    <Stats objects={responseStats} {layout} />
</div>
