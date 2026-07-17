export interface BeatFile {
   path: string;
   content: string;
   metadata: {
     title?: string;
     summary?: string;
     currentPlotPoint?: string;
     emotionalTone?: 'sublime' | 'comic' | 'tragic';
     characters?: string[];
     location?: string;
     timestamp?: number;
   };
}

function loadBeatFile(filePath: string): Promise<BeatFile> {
 return new Promise((resolve, reject) => {
   fs.readFile(
     filePath,
     'utf-8',
     (err, data) => err ? reject(err) : resolve({
       path: filePath,
       content: data,
       metadata: parseMetaFromContent(data),
     })
    )
  );
}

function parseMetaFromContent(content: string): BeatFile['metadata'] {
 const meta: any = {};

 // Extract title from YAML frontmatter
 try {
   const yamlMatch = content.match(/---\n([\s\S]*?)\n---/);
   if (yamlMatch) {
     const yamlBody = yamlMatch[1];
     meta.title = extractYamlValue(yamlBody, 'title');
     meta.summary = extractYamlValue(yamlBody, 'summary');
   }
 } catch (e) {}

 // Extract emotional tone indicators
 if (content.includes('sublime') || content.includes('tragedy') || 
    content.includes('existential weight')) {
   meta.emotionalTone = 'sublime';
 } else if (content.includes('comic') || content.includes('humor') ||
    content.includes('lighthearted')) {
   meta.emotionalTone = 'comic';
 }

 return meta;
}

export async function generateDivergencePaths(
   beatFile: BeatFile,
   userAlteration: string
 ): Promise<DivergencePaths> {
   // Prompt engine layer implementation
   const dialecticPrompt = buildDialecticPrompt({
     beatFile,
     userAlteration,
     emotionalTone: beatFile.metadata.emotionalTone || 'sublime',
   });

   // Call DeepSeek-V4-flash (model selected for creative divergence)
   const response = await deepseekGenerate(
     dialecticPrompt,
     { 
       model: 'deepseek-v4-flash',
       temperature: 0.85,
       top_p: 0.9,
     }
   );

   return parseDivergenceResponse(response);
}