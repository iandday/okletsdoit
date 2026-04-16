<script lang="ts">
    import type { RsvpStatsSchema } from "../../../api-client";
    import Stats from "./Stats.svelte";

    interface InviteStatsProps {
        rsvpStats: RsvpStatsSchema;
        layout?: "horizontal" | "vertical";
    }

    const { rsvpStats, layout = "vertical" }: InviteStatsProps = $props();
    const inviteStats = $derived([
        {
            title: "Invited",
            value: rsvpStats.totalInvited,
            icon: "mail",
        },
        {
            title: "Responded",
            value: rsvpStats.totalAttending + rsvpStats.totalDeclined,
            icon: "mail-open",
        },
    ]);
</script>

<div class="flex {layout === 'horizontal' ? 'flex-row' : 'flex-col'} gap-6 w-full justify-center">
    <Stats objects={inviteStats} {layout} />
</div>
