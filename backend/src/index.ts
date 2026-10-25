import express from "express";
import { authRouter } from "./routes/auth.ts";
import { projectsRouter } from "./routes/projects.ts";
import { promptStateRouter } from "./routes/promptState.ts";
import { trialRouter } from "./routes/trial.ts";
import { publicRouter } from "./routes/public.ts";
import { paddleWebhookRouter } from "./routes/webhooks/paddle.ts";

const app = express();
app.disable("x-powered-by");

// El webhook de Paddle necesita el body CRUDO (texto, no JSON ya
// parseado) para verificar la firma HMAC -- por eso se monta con su
// propio parser de texto, antes del express.json() global que aplica a
// todo lo demas.
app.use(
  "/api/webhooks/paddle",
  express.text({ type: () => true, limit: "1mb" }),
  paddleWebhookRouter,
);

app.use(express.json({ limit: "1mb" }));

app.use("/api/auth", authRouter);
app.use("/api/projects", projectsRouter);
app.use("/api/project-prompt-state", promptStateRouter);
app.use("/api/trial", trialRouter);
app.use("/api", publicRouter);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
app.use((err: unknown, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error("Error no manejado:", err);
  res.status(500).json({ error: "Error interno" });
});

const port = Number(process.env.PORT ?? 8787);
app.listen(port, () => {
  console.log(`Backend AI-SDLC Pro escuchando en :${port}`);
});
