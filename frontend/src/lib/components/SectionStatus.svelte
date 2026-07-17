<script lang="ts">
    type ISectionStatus = {
        enabled: boolean;
        visible: boolean;
        enabledTrueLabel?: string;
        enabledFalseLabel?: string;
        visibleTrueLabel?: string;
        visibleFalseLabel?: string;
    };

    const {
        enabled,
        visible,
        enabledTrueLabel = "Enabled",
        enabledFalseLabel = "Disabled",
        visibleTrueLabel = "Visible",
        visibleFalseLabel = "Hidden",
    }: ISectionStatus = $props();
</script>

{#if enabled}
    <div class="badge badge-success badge-lg">{enabledTrueLabel}</div>
{:else}
    <div class="badge badge-warning badge-lg">{enabledFalseLabel}</div>
{/if}
{#if visible}
    <div class="badge badge-success badge-lg">{visibleTrueLabel}</div>
{:else}
    <div class="badge badge-warning badge-lg">{visibleFalseLabel}</div>
{/if}
