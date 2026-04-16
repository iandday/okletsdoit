<script lang="ts">
    import type { GuestGroupSchema } from "../../../api-client";
    import type { IStat } from "../../types";
    import Stats from "./Stats.svelte";

    interface GuestListStatsProps {
        guestGroups: GuestGroupSchema[];
    }
    const { guestGroups }: GuestListStatsProps = $props();

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

<div class="flex flex-col md:flex-row gap-6 w-full justify-center">
    <Stats objects={guestStats} />
</div>
