def architecture_gate(target,sources):
 required=("vendor","backend","device_sku","architecture_id","sdk_version")
 if any(not target.get(k) for k in required): return {"status":"BLOCKED_NO_OFFICIAL_ARCH","missing":list(required)}
 if not sources or not all(s.get("url") and s.get("title") and "diagram_verified" in s for s in sources): return {"status":"BLOCKED_NO_OFFICIAL_ARCH","missing":["official_sources"]}
 return {"status":"ARCH_RESEARCH_COMPLETE","sources":sources}
