#ifndef CHANNEL_H
#define CHANNEL_H

#include <casdef.h>
#include <asLib.h>

class PV;

class Channel : public casChannel {
    public:
        Channel(const casCtx &ctxIn,  PV *pvIn,
                const char * const pUserNameIn,
                const char * const pHostNameIn);
        ~Channel();

        /* server library calls these methods to determine
         * client's access rights.
         */
        virtual bool readAccess() const;
        virtual bool writeAccess() const;

        /* server library calls these methods to write PV (asynchronousely).
         */
        virtual caStatus write (const casCtx &ctx, const gdd &value);
        virtual caStatus writeNotify (const casCtx &ctx, const gdd &value);
    private:
        Channel & operator = ( const Channel & );
        Channel ( const Channel & );

        PV * pPv;
        char * pUserName;
        char * pHostName;

        ASCLIENTPVT client;
};

#endif
