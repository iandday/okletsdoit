<script lang="ts">
    type IPageTitle = {
        label?: string;
        title?: string;
        description?: string;
        centered?: boolean;
        image?: string;
    };

    const { label, title, description, centered = true, image }: IPageTitle = $props();
</script>

<div class={centered ? "text-center pt-4" : "pt-4"}>
    {#if image}
        <div class="flex justify-center mb-2">
            <img src={image} alt="page-title-image" class="max-w-sm rounded-lg justify-self-center" />
        </div>
    {/if}
    {#if label}
        <div class="badge bg-base-100 badge-outline border-base-300 badge-sm font-mono">{label}</div>
    {/if}
    {#if title}
        <p
            class="text-center text-4xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-4xl 2xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent mb-4">
            {title}
        </p>
    {/if}
    <div class="mt-2 flex items-center justify-center">
        {#if description}
            <p class="text-base-content/70 text-xl italic max-w-2xl mx-auto">{description}</p>
        {/if}
    </div>
</div>
