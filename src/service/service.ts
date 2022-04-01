import {Class, Feedback, FeedbackUtil} from "../models";
import {UploadedFile} from "express-fileupload";
import {database, MongoCollection} from "../database/database";
import {ResponseError} from "../rest/middleware";
import {ResponseMessage, StatusCode} from "../rest/rest.utils";

export class Service {

    static async getMaterials(): Promise<Class[]> {
        const materialsCollection = database.collection(MongoCollection.MATERIALS);
        const materialsCursor = await materialsCollection.find();
        return (await materialsCursor.toArray()) as unknown as Class[];
    }

    static async refreshMaterials(jsonFile: UploadedFile): Promise<void> {
        const jsonStr = jsonFile.data.toString('utf8');
        const materials: Class[] = JSON.parse(jsonStr).map((item: Class) => {
            return {...item, updatedAt: new Date(item.updatedAt)};
        });

        const materialsCollection = database.collection(MongoCollection.MATERIALS);

        await materialsCollection.deleteMany({});
        console.log('All materials deleted');
        await materialsCollection.insertMany(materials);
        console.log('Materials inserted');
    }

    static async getFeedback(): Promise<Feedback[]> {
        const feedbackCollection = database.collection(MongoCollection.FEEDBACK);
        const feedbackCursor = await feedbackCollection.find();
        return (await feedbackCursor.toArray()) as unknown as Feedback[];
    }

    static async addFeedback(feedback: Feedback): Promise<void> {
        if (!FeedbackUtil.checkFeedback(feedback)) {
            throw new ResponseError(ResponseMessage.FORM_SHOULD_MEET_THE_CONSTRAINTS, StatusCode.BAD_REQUEST);
        }

        const feedbackCollection = database.collection(MongoCollection.FEEDBACK);
        await feedbackCollection.insertOne(feedback);
    }

}