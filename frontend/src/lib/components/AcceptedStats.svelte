<script lang="ts">
    import type { RsvpStatsSchema, WeddingSettingsSchema } from "../../../api-client";
    import type { IStat } from "../../types";
    import Stats from "./Stats.svelte";

    interface AcceptedStatsProps {
        rsvpStats: RsvpStatsSchema;
        configData: WeddingSettingsSchema;
        layout?: "horizontal" | "vertical";
    }

    const { rsvpStats, configData, layout = "vertical" }: AcceptedStatsProps = $props();

    const statsValues: IStat[] = [
        {
            title: configData.standardGroupLabel,
            value: rsvpStats.totalStandardAccepted,
            icon: "users",
        },
    ];

    if (configData.rsvpShowAccommodationIntro) {
        statsValues.push({
            title: configData.accommodationGroupLabel,
            value: rsvpStats.totalAccommodation,
            icon: "building",
        });
    }

    if (configData.rsvpShowVipIntro) {
        statsValues.push({
            title: configData.vipGroupLabel,
            value: rsvpStats.totalVipAccepted,
            icon: "star",
        });
    }
</script>

<div class="flex {layout === 'horizontal' ? 'flex-row' : 'flex-col'} gap-6 w-full justify-center">
    <Stats objects={statsValues} {layout} />
</div>
