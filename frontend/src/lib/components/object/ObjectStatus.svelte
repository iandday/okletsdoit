<script lang="ts">
    type IObjectStatus = {
        status: boolean;
        text: string;
    };

    const { status, text }: IObjectStatus = $props();
</script>

{#if status}
    <div class="badge badge-success badge-lg">✓ {text}</div>
{:else}
    <div class="badge badge-warning badge-lg">⏳ {text}</div>
{/if}
