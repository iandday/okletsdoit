<script lang="ts">
    type iViewDetailsProps = {
        href: string;
        label?: string | null;
        size?: "sm" | "md" | "lg";
    };

    const { href, label = null, size = "md" }: iViewDetailsProps = $props();

    const sizeClasses = {
        sm: "btn-sm gap-1",
        md: "btn-md gap-2",
        lg: "btn-lg gap-3",
    };

    const iconSizes = {
        sm: "size-4",
        md: "size-5",
        lg: "size-6",
    };
</script>

<a {href} class="btn btn-accent {sizeClasses[size]}"
    ><span class="icon-[lucide--eye] {iconSizes[size]}"></span>
    {#if label}{label}{/if}
</a>
