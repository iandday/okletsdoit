<script lang="ts">
    type iEditObjectProps = {
        href: string;
        label?: string;
        size?: "sm" | "md" | "lg";
    };

    const { href, label, size = "md" }: iEditObjectProps = $props();

    const sizeClasses = {
        sm: "btn-sm gap-1",
        md: "btn-md gap-2",
        lg: "btn-lg gap-3",
    };

    const iconSizes = {
        sm: "size-4",
        md: "size-6",
        lg: "size-7",
    };
</script>

<button class="btn btn-success {sizeClasses[size]}" onclick={() => (window.location.href = href)}>
    <span class="icon-[lucide--edit] {iconSizes[size]}"></span>
    {#if label}{label}{/if}
</button>
