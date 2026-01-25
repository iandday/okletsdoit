<script lang="ts">
    import { enhance } from "$app/forms";
    import type { input } from "motion/react-client";

    type iDeleteObjectProps = {
        href: string;
        label?: string;
        action: string;
        value: string | number;
        confirmMessage?: string;
    };

    const { href, label, action, value, confirmMessage }: iDeleteObjectProps = $props();
</script>

<form
    method="POST"
    {action}
    use:enhance={() => {
        return async ({ update }) => {
            if (confirm(confirmMessage)) {
                await update();
            }
        };
    }}>
    <input type="hidden" name="value" {value} />
    <button type="submit" class="btn btn-sm btn-error" title="Remove">
        {#if label}
            <span>{label}</span>
        {/if}
        <span class="icon-[lucide--trash] size-4"></span>
    </button>
</form>
