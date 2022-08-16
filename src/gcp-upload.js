/**
 * This is internal-only script that uploads all models to Google Cloud Storage bucket
*/

/* GCP bucket auth init
  gcloud iam service-accounts create human-storage-admin
  gcloud projects add-iam-policy-binding protean-keyword-350712 --member="serviceAccount:human-storage-admin@protean-keyword-350712.iam.gserviceaccount.com" --role=roles/storage.admin
  gcloud iam service-accounts keys create human-service-account.json --iam-account=human-storage-admin@protean-keyword-350712.iam.gserviceaccount.com
*/

const fs = require('fs');
const path = require('path');
const log = require('@vladmandic/pilogger');
const { Storage } = require('@google-cloud/storage');
const authJson = require('../secret/human-service-account.json');

const keyFilename = 'secret/human-service-account.json';
const bucketName = 'human-models';
const localDir = 'models';

async function main() {
  log.headerJson();
  const storage = new Storage({ projectId: authJson.project_id, keyFilename });
  const [buckets] = await storage.getBuckets();
  let bucket = buckets.find((b) => b.name === bucketName);
  let bucketMetadata = {};
  if (!bucket) {
    [bucket, bucketMetadata] = await storage.createBucket(bucketName);
    await storage.bucket(bucketName).makePublic();
  } else {
    [bucketMetadata] = await storage.bucket(bucketName).getMetadata();
  }
  log.data('bucket metadata:', bucketMetadata);
  let [bucketFiles] = await storage.bucket(bucketName).getFiles();
  const dir = fs.readdirSync(localDir);
  log.state('enumerating:', { folder: localDir, files: dir.length });
  for (const f of dir) {
    // if (f !== 'README.md') continue;
    const p = path.join(localDir, f);
    const stat = fs.statSync(p);
    let bucketFile = bucketFiles.find((each) => each.name === f);
    if (bucketFile?.metadata?.metadata?.ctimeMs === stat.ctimeMs.toString()) {
      log.data('exists:', { file: p, url: `https://storage.googleapis.com/${bucketName}/${f}`, size: bucketFile.metadata.size }); // link: uploaded.metadata.mediaLink
    } else {
      [bucketFile] = await storage.bucket(bucketName).upload(path.join(localDir, f), { destination: f, gzip: true, public: true });
      await bucketFile.setMetadata({ metadata: { ctimeMs: stat.ctimeMs.toString() } });
      log.data('upload:', { file: p, url: `https://storage.googleapis.com/${bucketName}/${f}` });
    }
  }
  for (const f of bucketFiles) {
    if (!dir.includes(f.name)) {
      await f.delete();
      log.data('delete', f.name);
    }
  }
  [bucketFiles] = await storage.bucket(bucketName).getFiles();
  const totalSize = bucketFiles.reduce((prev, curr) => prev + parseInt(curr.metadata.size), 0);
  log.info('bucket info:', { files: bucketFiles.length, size: totalSize });
}

main();
