// Flujo de OAuth con GitHub, implementado a mano. El riesgo real de este
// archivo es CSRF en el callback si `state` no se valida correctamente --
// por eso authorizeUrl() y validateState() siempre van en pareja (ver
// backend/src/routes/auth.ts).
import { randomBytes } from "node:crypto";

interface GithubOAuthConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
}

function config(): GithubOAuthConfig {
  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const clientSecret = process.env.GITHUB_OAUTH_CLIENT_SECRET;
  const publicBaseUrl = process.env.PUBLIC_BASE_URL;
  if (!clientId || !clientSecret || !publicBaseUrl) {
    throw new Error(
      "GITHUB_OAUTH_CLIENT_ID / GITHUB_OAUTH_CLIENT_SECRET / PUBLIC_BASE_URL no configurados",
    );
  }
  return { clientId, clientSecret, redirectUri: `${publicBaseUrl}/api/auth/callback` };
}

export function generateState(): string {
  return randomBytes(24).toString("hex");
}

export function authorizeUrl(state: string): string {
  const { clientId, redirectUri } = config();
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: "read:user",
    state,
  });
  return `https://github.com/login/oauth/authorize?${params.toString()}`;
}

export interface GithubUser {
  githubId: string;
  githubLogin: string;
  email: string | null;
}

export async function exchangeCodeForUser(code: string): Promise<GithubUser> {
  const { clientId, clientSecret, redirectUri } = config();

  const tokenResponse = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      code,
      redirect_uri: redirectUri,
    }),
  });
  if (!tokenResponse.ok) {
    throw new Error(`GitHub token exchange fallo con status ${tokenResponse.status}`);
  }
  const tokenData = (await tokenResponse.json()) as {
    access_token?: string;
    error?: string;
    error_description?: string;
  };
  if (!tokenData.access_token) {
    throw new Error(`GitHub token exchange sin access_token: ${tokenData.error_description ?? tokenData.error ?? "desconocido"}`);
  }

  const userResponse = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: `Bearer ${tokenData.access_token}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "ai-sdlc-pro-backend",
    },
  });
  if (!userResponse.ok) {
    throw new Error(`GitHub /user fallo con status ${userResponse.status}`);
  }
  const userData = (await userResponse.json()) as {
    id: number;
    login: string;
    email: string | null;
  };

  return {
    githubId: String(userData.id),
    githubLogin: userData.login,
    email: userData.email,
  };
}
