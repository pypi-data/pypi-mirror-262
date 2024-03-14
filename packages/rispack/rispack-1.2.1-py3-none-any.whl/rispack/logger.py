from aws_lambda_powertools import Logger as PowertoolsLogger

from rispack.schemas import BaseSchema, mask_data


class Logger(PowertoolsLogger):
    def mask_info(self, data, mask=None):
        if isinstance(data, BaseSchema):
            data = data.dump()

        if isinstance(mask, dict):
            data = mask_data(data, mask)
        else:
            data = mask_data(data)

        return self.info(data)


logger = Logger()
