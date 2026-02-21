import { exportRegistry, type ExportFormat, type ExportResourceType } from "$lib/server/export-registry";
import { error } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ url }) => {
    const resource = url.searchParams.get("resource") as ExportResourceType | null;
    const format = (url.searchParams.get("format") as ExportFormat) || "csv";
    const fileName = url.searchParams.get("fileName");

    if (!resource || !exportRegistry[resource]) {
        throw error(400, `Invalid resource type: ${resource}`);
    }

    if (format !== "csv" && format !== "xlsx") {
        throw error(400, `Invalid format: ${format}`);
    }

    const config = exportRegistry[resource];

    try {
        const blob = await config.exportFn(format);
        const finalFileName = fileName || `${config.defaultFileName}.${format}`;

        return new Response(blob, {
            headers: {
                "Content-Type": config.contentType[format],
                "Content-Disposition": `attachment; filename="${finalFileName}"`,
            },
        });
    } catch (err) {
        console.error(`Export failed for ${resource}:`, err);
        throw error(500, `Failed to export ${resource} data`);
    }
};
