import { createClient, RedisClientType, SchemaFieldTypes, VectorAlgorithms } from 'redis';

export class RedisSimilarity {

    private _client 

    constructor(connectionString: string, password: string) {
        this._client = createClient({
            url: connectionString,
            password: password
        });
    }

    public connect = async () => {
        await this._client.connect()
    }

    public disconnect = async () => {
        await this._client.disconnect()
    }

    public dropIndex = async (indexName: string) => {
        await this.flushall()
        let out
        try {
            out = await this._client.ft.dropIndex(indexName)
        } catch (e) {
            console.log(e)
        }
        return out
    }

    public createIndex = async (indexName: string, dimension: number) => {
        let out
        try {
            //out = await this._client.ft.dropIndex(indexName)
            out = await this._client.ft.create(indexName, {
                v: {
                    type: SchemaFieldTypes.VECTOR,
                    ALGORITHM: VectorAlgorithms.HNSW,
                    TYPE: 'FLOAT32',
                    DIM: dimension,
                    DISTANCE_METRIC: 'COSINE'
                },
                pipeline : SchemaFieldTypes.TEXT
            }, {
                ON: 'HASH'
            });
        } catch (e) {
            if (e.message === 'Index already exists') {
                console.log('Index exists already, skipped creation.');
            }else{
                console.log(e)
            }
        }
        return out
    }

    public set = async (id: string, document: any, embeddings: any) => {
        await this._client.hSet(id, {v : this._float32Buffer(embeddings), pipeline: document.pipeline.replace('-','')})
    }

    public query = async (indexName: string, embeddings: any, numResults: string, pipeline: string) => {
        return await this._client.ft.search(indexName, `(@pipeline:${pipeline.replace('-','')})=>[KNN ${numResults} @v $BLOB AS dist]`, {
            PARAMS: {
                BLOB: this._float32Buffer(embeddings)
            },
            SORTBY: 'dist',
            DIALECT: 2,
            RETURN: ['dist','pipeline']
        });
    }

    public flushall = async () => {
        return await this._client.sendCommand(['FLUSHALL']);;
    }

    public getKeys = async () => {
        return await this._client.sendCommand(['KEYS','*']);;
    }

    private _float32Buffer = (arr) => {
        return Buffer.from(new Float32Array(arr).buffer);
    }
}