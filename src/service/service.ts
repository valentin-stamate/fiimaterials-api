import {Class} from "../models";
import {UploadedFile} from "express-fileupload";
import {database, MongoCollection} from "../database/database";

export class Service {

    static async getMaterials(): Promise<Class[]> {
        const materialsCollection = database.collection(MongoCollection.MATERIALS);
        const materialsCursor = await materialsCollection.find();
        return (await materialsCursor.toArray()) as unknown as Class[];
    }

    static async refreshMaterials(jsonFile: UploadedFile): Promise<void> {
        const jsonStr = jsonFile.data.toString('utf8');
        const materials: Class[] = JSON.parse(jsonStr);

        const materialsCollection = database.collection(MongoCollection.MATERIALS);

        await materialsCollection.deleteMany({});
        console.log('All materials deleted');
        await materialsCollection.insertMany(materials);
        console.log('Materials inserted');
    }

}