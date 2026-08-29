<script lang="ts">
    import type { GuestGroupSchema } from "../../../api-client";
    import type { IStat } from "../../types";
    import Stats from "./Stats.svelte";

    interface GuestListStatsProps {
        guestGroups: GuestGroupSchema[];
        layout?: "horizontal" | "vertical";
    }
    const { guestGroups, layout = "horizontal" }: GuestListStatsProps = $props();

    const guestStats = $derived([
        {
            title: "Guest Groups",
            value: guestGroups.length,
            //description: `of ${guestGroups.length} total`,
            icon: "users",
        },
        {
            title: "Guests",
            value: guestGroups.reduce((sum, group) => sum + group.groupCount, 0),
            //description: `of ${guestGroups.reduce((sum, group) => sum + group.groupCount, 0)} total`,
            icon: "user",
        },
    ]);
</script>

<div class="flex {layout === 'horizontal' ? 'flex-row' : 'flex-col'} gap-6 justify-center">
    <Stats objects={guestStats} {layout} />
</div>
