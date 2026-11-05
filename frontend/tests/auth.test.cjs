const { test } = require("node:test");
const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const Module = require("node:module");
const ts = require("typescript");
const { NextRequest } = require("next/server");
const file = require("node:path").resolve(__dirname, "../proxy.ts");
const compiled = ts.transpileModule(readFileSync(file, "utf8"), { compilerOptions: { module: ts.ModuleKind.CommonJS } }).outputText;
const mod = new Module(file, module);
mod.filename = file;
mod.paths = module.paths;
mod._compile(compiled, file);
const { proxy } = mod.exports;

test("cloud access protects data and scopes worker credentials", () => {
  const previousPassword = process.env.WORKSPACE_PASSWORD;
  const previousKey = process.env.API_KEY;
  try {
    process.env.WORKSPACE_PASSWORD = "long-test-password";
    process.env.API_KEY = "test-machine-credential";
    const request = (path, headers = {}) => proxy(new NextRequest(`https://app.example${path}`, { headers }));
    assert.equal(request("/").status, 401);
    assert.equal(request("/api/vocab").status, 401);
    assert.equal(request("/api/vocab", { "X-API-Key": process.env.API_KEY }).status, 401);
    assert.equal(request("/api/cloud/jobs/job-id", { "X-API-Key": process.env.API_KEY }).status, 200);
    assert.equal(request("/api/cloud/jobsx/job-id", { "X-API-Key": process.env.API_KEY }).status, 401);
    assert.equal(request("/api/cloud/jobs/job-id", { "X-API-Key": "wrong" }).status, 401);
    assert.equal(request("/api/health").status, 200);
    const authorization = "Basic " + Buffer.from("codelingo:long-test-password").toString("base64");
    assert.equal(request("/api/vocab", { authorization }).status, 200);
    delete process.env.WORKSPACE_PASSWORD;
    assert.equal(request("/").status, 200);
  } finally {
    if (previousPassword === undefined) delete process.env.WORKSPACE_PASSWORD; else process.env.WORKSPACE_PASSWORD = previousPassword;
    if (previousKey === undefined) delete process.env.API_KEY; else process.env.API_KEY = previousKey;
  }
});
