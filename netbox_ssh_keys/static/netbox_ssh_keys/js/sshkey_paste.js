/**
 * Auto-parse pasted SSH public key lines.
 *
 * When a user pastes a full authorized_keys line such as:
 *   ssh-ed25519 AAAAC3Nza... user@host
 *
 * This script:
 *  - Detects the key type prefix and sets the Type dropdown
 *  - Extracts the comment and sets the Name field (if empty)
 *  - Strips the key to base64-only in the Public Key textarea
 */
(function () {
    'use strict';

    const KNOWN_KEY_TYPES = [
        'ssh-rsa',
        'ssh-ed25519',
        'ecdsa-sha2-nistp256',
        'ecdsa-sha2-nistp384',
        'ecdsa-sha2-nistp521',
        'sk-ssh-ed25519@openssh.com',
        'sk-ecdsa-sha2-nistp256@openssh.com',
    ];

    function parseAndDistribute(textarea) {
        const value = textarea.value.trim();
        if (!value) return;

        const parts = value.split(/\s+/);
        if (parts.length < 2) return;

        const maybeType = parts[0];
        if (!KNOWN_KEY_TYPES.includes(maybeType)) return;

        // We have a full key line — split it up
        const keyType = parts[0];
        const keyMaterial = parts[1];
        const comment = parts.slice(2).join(' ');

        // Set the public_key field to base64-only
        textarea.value = keyMaterial;

        // Set the key_type dropdown (NetBox wraps selects with TomSelect)
        const typeSelect = document.getElementById('id_key_type');
        if (typeSelect) {
            if (typeSelect.tomselect) {
                typeSelect.tomselect.setValue(keyType, true);
            } else {
                typeSelect.value = keyType;
                typeSelect.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }

        // Set the name field if it's empty
        if (comment) {
            const nameInput = document.getElementById('id_name');
            if (nameInput && !nameInput.value.trim()) {
                nameInput.value = comment;
                nameInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        const textarea = document.getElementById('id_public_key');
        if (!textarea) return;

        // Handle paste events
        textarea.addEventListener('paste', function (e) {
            // Let the paste happen, then process on next tick
            setTimeout(function () {
                parseAndDistribute(textarea);
            }, 0);
        });

        // Also handle input (e.g., drag-and-drop or typing then tabbing)
        textarea.addEventListener('blur', function () {
            parseAndDistribute(textarea);
        });
    });
})();
